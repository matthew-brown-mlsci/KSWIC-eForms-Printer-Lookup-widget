"""

KSWIC eForms Printer Lookup service

"""

import pyad.adquery
import pyad.pyad
import pyad.pyadutils
import pythoncom

import base64
import struct

from kswic_config import *
from kswic_api import *
from kswic_objs import *
from sqlite_cache import *
from active_directory import *

@jsonp
def ListKnownDomains():
    domain_objs = []
    try:
        with open(domain_config_file, 'r') as f:
            line = f.readline()
            while line:
                line_domain = line.split('|')[1]
                line_base_dn = line.split('|')[3].strip()
                line_ldap_servers = line.split('|')[5].strip().split(';')
                d = domain_obj(domain=line_domain,base_dn=line_base_dn,ldap_servers=line_ldap_servers[:])
                domain_objs.append(d)
                line = f.readline()
    except Exception as e:
        return jsonify(success=False,
                  error=("Error loading domain_config_file: " + domain_config_file),
                  exception=str(e))

    return jsonify(success=True,
                   domains=[e.serialize() for e in domain_objs])

#@app.route("/GroupUsers", methods=['GET'])
@jsonp
def GroupUsers():
    domain = request.args.get('domain')
    group = request.args.get('group')
    last_exception = None

    if domain and group:
        try:
            domain_objs = []
            with open(domain_config_file, 'r') as f:
                line = f.readline()
                while line:
                    line_domain = line.split('|')[1]
                    line_base_dn = line.split('|')[3].strip()
                    line_ldap_servers = line.split('|')[5].strip().split(';')
                    d = domain_obj(domain=line_domain,base_dn=line_base_dn,ldap_servers=line_ldap_servers[:])
                    domain_objs.append(d)
                    line = f.readline()
            domain_set = [e.serialize() for e in domain_objs]
            domain_check = next((item for item in domain_set if item["domain"] == domain), None)
            if not domain_check:
                return jsonify(success=False,
                               error=("'domain' parameter '" + domain + "' not present in domain_config_file"))
            base_dn = domain_check['base_dn']
            ldap_servers = domain_check['ldap_servers']
            
        except Exception as e:
            return jsonify(success=False,
                    error=("Error loading domain_config_file: " + domain_config_file),
                    exception=str(e))

        # Now try the AD query
        ldap_server_query_success = 0
        for ldap_server in ldap_servers:
            pyad.pyad_setdefaults(ldap_server=ldap_server)
            if ldap_server_query_success == 0:
                try:
                    query_results = []
                    pythoncom.CoInitialize()

                    q = pyad.adquery.ADQuery()
                    q.execute_query(
                        attributes=["distinguishedName"],
                        where_clause="objectClass = 'group' AND cn = '{}'".format(group),
                        base_dn=base_dn
                    )
                    
                    if q.get_row_count() == 0:
                        return jsonify(success=False,
                                domain=domain,
                                group=group,
                                ldap_server=ldap_server,
                                error='No rows returned from adsi query')

                    group_dn = ''
                    for row in q.get_results():
                        group_dn = row['distinguishedName']
                    ldap_server_query_success = 1

                except Exception as e:
                    last_exception = e

            if last_exception:
                pythoncom.CoUninitialize()
                return jsonify(success=False,
                               error=("Error querying domain controller"),
                               ldap_server=ldap_server,
                               domain=domain,
                               group=group,
                               exception=str(last_exception))
            
            if group_dn == '':
                pythoncom.CoUninitialize()
                return jsonify(success=False,
                        error=("Error group cn specified invalid"),
                        domain=domain,
                        group=group
                        )

            if ldap_server_query_success == 1:
                try:
                    q = pyad.adquery.ADQuery()
                    q.execute_query(
                                    attributes=["distinguishedName", "sAMAccountName"],
                                    where_clause="memberOf = '{}'".format(group_dn),
                                    base_dn=base_dn
                                )

                    # parse the user dn/samaccountname results
                    users = []
                    for row in q.get_results():
                        users.append({"distinguishedName": row['distinguishedName'],
                                    "sAMAccountName": row['sAMAccountName'] })
                    pythoncom.CoUninitialize()
                    return jsonify(success=True,
                                domain=domain,
                                group=group,
                                ldap_server=ldap_server,
                                group_dn=group_dn,
                                users=[e for e in users])


                except Exception as e:
                    return jsonify(success=False,
                                    error=("Error querying domain controller for memberOf information"),
                                    domain=domain,
                                    group=group,
                                    ldap_server=ldap_server,
                                    exception=str(e))

    else:
        return jsonify(success=False,
                       error="/GroupUsers requires parameter 'domain', and 'group'")

#  Takes domain + user id request arg, checks against sqlite db file.  If no entry in that file, 
#  runs AD check per service config file.  Reduces wait times for calls that require AD auth, returns
#  access code, either read-only or read-write
#
#
#   check args
#   check if sql db cache file exists
#   (new def) create if not exists
#   (new def) If exists check for data (query with timestamp less-than) and return data
#   (new def) Check AD
#       load domains.conf
#       query AD (use list of domain controllers)
#       return success, data
#   If AD success, insert or update data into sql db cache file
#       else return error codes
#   return data

def validate_domain(domain):
    try:
        domain_objs = []
        with open(domain_config_file, 'r') as f:
            line = f.readline()
            while line:
                line_domain = line.split('|')[1]
                line_base_dn = line.split('|')[3]
                line_ldap_servers = line.split('|')[5].strip().split(';')
                d = domain_obj(domain=line_domain,base_dn=line_base_dn,ldap_servers=line_ldap_servers[:])
                domain_objs.append(d)
                line = f.readline()
        domain_set = [e.serialize() for e in domain_objs]
        domain_check = next((item for item in domain_set if item["domain"] == domain), None)
        if not domain_check:
            return None, None, ('supplied domain: ' + domain + ' not found in domain_config_file: ' + domain_config_file)
        base_dn = domain_check['base_dn']
        ldap_servers = domain_check['ldap_servers']
        return base_dn, ldap_servers, None
    except Exception as e:
        return None, None, str(e)

# Loop through list of ldap servers attempting to query memberOf + cn given samAccountName
def ad_query_memberOf(base_dn, ldap_servers, samAccountName):
    #print("ad_query_memberOf(base_dn, ldap_servers, samAccountName)")
    #print("(" + base_dn + ", " + str(ldap_servers) + ", " + samAccountName)
    ldap_server_query_success = 0
    for ldap_server in ldap_servers:
        pyad.pyad_setdefaults(ldap_server=ldap_server)
        if ldap_server_query_success == 0:
            try:
                query_results = []
                pythoncom.CoInitialize()

                q = pyad.adquery.ADQuery()
                q.execute_query(
                                attributes=["sAMAccountName",
                                            "memberOf",
                                            "name",
                                            "cn"],
                                where_clause="samAccountName = '{}'".format(samAccountName),
                                base_dn=base_dn
                            )
                
                if q.get_row_count() == 0:
                    ldap_server_query_success = 1
                    return None, None, 'No rows returned from adsi query'
                
                cn = None
                group_count = 0
                groups = []
                for row in q.get_results():
                    
                    for attr in row:
                        print(str(row[attr]))
                        if attr == 'cn':
                            cn = str(row[attr])
                        if attr == 'name':
                            name = str(row[attr])
                        if attr == 'memberOf':
                            for member in row[attr]:
                                full_cn = member
                                member_of_group = member.split(',')[0].split('=')[1]
                                groups.append({
                                                "group":member_of_group,
                                                "full_cn":full_cn
                                })
                                group_count = group_count + 1

                if not cn:
                    ldap_server_query_success = 1
                    pythoncom.CoUninitialize()
                    return None, None, 'samAccountName not found'
                pythoncom.CoUninitialize()
                ldap_server_query_success = 1
                
            except Exception as e:
                last_exception = e
                
    if ldap_server_query_success == 0:
        return None, None, ("Error querying domain controller: " + str(last_exception))
    else:
        #print("cn, groups")
        #print(str(cn) + ", " + str(groups))
        return cn, groups, None

def access_for_user(memberOf, config, samAccountName, domain):
    #print("access_for_user(memberOf, config, samAccountName, domain)")
    #print(str(memberOf) + ", " + str(config) + ", " + str(samAccountName + ", " + str(domain)))
    access_level = None
    ad_resource = None
    access_from_user_or_group = None
    # Check users first
    for config_user in config['allowed_ad_users']:
        if (config_user['ad_user'].upper() == samAccountName.upper()) and (config_user['domain'].upper() == domain.upper()):
            #print("found! config_user: " + config_user['domain'] + "\\" + config_user['ad_user'] + "   against samAccountName: " + samAccountName)
            access_level = config_user['access_level']
            access_from_user_or_group = 'ad_user'
            ad_resource = config_user['domain'] + "\\" + config_user['ad_user']

    if access_level:
        return access_level, access_from_user_or_group, ad_resource
    
    # Then check groups
    for config_group in config['allowed_ad_groups']:
        for memberOf_group in memberOf:
            if (config_group['ad_group'].upper() == memberOf_group['group'].upper()) and (config_group['domain'].upper() == domain.upper()):
                print("found! config_group: " + config_group['domain'] + "\\" + config_group['ad_group'] + "   against memberOf_group: " + memberOf_group['group'])
                access_level = config_group['access_level']
                access_from_user_or_group = 'ad_group'
                ad_resource = config_group['domain'] + "\\" + config_group['ad_group']
     
    if access_level:
        return access_level, access_from_user_or_group, ad_resource
        
    # returns None (no acces), read-only, or read-write
    return access_level, access_from_user_or_group, ad_resource


#@app.route("/verifyUserAccess", methods=['GET'])
@jsonp
def verifyUserAccess():
    domain = request.args.get('domain')
    samAccountName = request.args.get('samAccountName')

    if not domain:
        return jsonify(success=False,
                       error="/verifyUserAccess requires parameter 'domain', and 'samAccountName'")
    if not samAccountName:
        return jsonify(success=False,
                       error="/verifyUserAccess requires parameter 'domain', and 'samAccountName'")
    

    fn = sqlite_cache_file
    if not create_sqlite_cache_if_not_exist(fn):
        return jsonify(success=False,
                       error=("Cannot create sqlite db file: " + fn))
    else:
        cached_record = query_sqlite_cache_one_row(domain, samAccountName)
    
    # If user was cached, return what's in the SQLite db, else to the AD lookup and place in SQLite cache
    if cached_record:
        
        passkey = cached_record[2]
        access_level = cached_record[4]
        access_from_user_or_group = cached_record[5]
        ad_resource = cached_record[6]

        return jsonify(success=True,
                       samAccountName=samAccountName,
                       domain=domain,
                       passkey=passkey,
                       access_level=access_level,
                       access_from_user_or_group=access_from_user_or_group,
                       ad_resource=ad_resource,
                       cached_access=True)

    else:
        # Check if supplied domain argument is valid & we have a domain controller on-file to query
        base_dn, ldap_servers, verify_error = validate_domain(domain)
        if not base_dn:
            return jsonify(success=False,
                    error=("Error verifying domain: " + verify_error))

        # Now try the AD query
        cn, memberOf, ad_query_error = ad_query_memberOf(base_dn, ldap_servers, samAccountName)
        if not cn:
            return jsonify(success=False,
                    error=("Error querying AD controller: " + ad_query_error))
         
        # Load config file and verify contents
        config = loadConfigFile()
        if ('error' in config):
            return jsonify(success=False,
                           error="error loading config file",
                           config=str(config))

        # Check if our samAccountName is a memberOf any of the groups in config
        # returns None (no acces), read-only, or read-write
        access_level, access_from_user_or_group, ad_resource = access_for_user(memberOf, config, samAccountName, domain)
        #print(access_level)
        #print(access_from_user_or_group)
        #print(ad_resource)

        if not access_level:
            return jsonify(success=False,
                           error=("Error '" + domain + "\\" + samAccountName + "' not configured in access file."))
        
        query_sqlite_cache_replace_row(samAccountName, domain, access_level, access_from_user_or_group, ad_resource)

        cached_record = query_sqlite_cache_one_row(domain, samAccountName)
        passkey = cached_record[2]
        access_level = cached_record[4]
        access_from_user_or_group = cached_record[5]
        ad_resource = cached_record[6]

        return jsonify(success=True,
                       samAccountName=samAccountName,
                       domain=domain,
                       passkey=passkey,
                       access_level=access_level,
                       access_from_user_or_group=access_from_user_or_group,
                       ad_resource=ad_resource,
                       cached_access=False)