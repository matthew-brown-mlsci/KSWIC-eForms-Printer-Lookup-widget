"""

KSWIC eForms Printer Lookup service

"""

from flask import Flask
from flask import render_template
import sys
import os
from os.path import exists
import time
import datetime
from flask import jsonify
import socket
from functools import wraps
from flask import redirect, request, current_app, app
import tempfile
import sqlite3
import math

import pytds
from pytds import login

import pyad.adquery
import pyad.pyad
import pyad.pyadutils
import pythoncom

import base64
import struct
from kswic_config import *
from kswic_objs import *
from sqlite_cache import *

@jsonp
def selectAllHospitalRows():
    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")
    
    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )

    try:
        with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                           user=config['database_username'], password=config['database_password']) as conn:
            with conn.cursor() as cur:
                sql = "SELECT hospital_key, pc_id, printer, notes, created, createdby, edited, editedby, inactivated, inactivatedby FROM " + config['database_name'] + ".dbo.hospital;"
                cur.execute(sql)
                allfetchedrows = cur.fetchall()
                rows = []
                for row in allfetchedrows:
                    if row[0]:
                        hospital_key = row[0]
                    else:
                        hospital_key = None
                    if row[1]:
                        pc_id = row[1].strip()
                    else:
                        pc_id = None
                    if row[2]:
                        printer = row[2].strip()
                    else:
                        printer = None
                    if row[3]:
                        notes = row[3].strip()
                    else:
                        notes = None
                    if row[4]:
                        created = row[4].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        created = None
                    if row[5]:
                        createdby = row[5].strip()
                    else:
                        createdby = None
                    if row[6]:
                        edited = row[6].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        edited = None
                    if row[7]:
                        editedby = row[7].strip()
                    else:
                        editedby = None
                    if row[8]:
                        inactivated = row[8].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        inactivated = None
                    if row[9]:
                        inactivatedby = row[9].strip()
                    else:
                        inactivatedby = None

                    rows.append({'id':hospital_key,
                                 'hospital_key':hospital_key,
                                 'pc_id':pc_id,
                                 'printer':printer,
                                 'notes':notes,
                                 'created':created,
                                 'createdby':createdby,
                                 'edited':edited,
                                 'editedby':editedby,
                                 'inactivated':inactivated,
                                 'inactivatedby':inactivatedby})

                return jsonify(success=True,
                               data=rows,
                               last_page=1)

    except Exception as e:
        return jsonify(success=False,
                error="Error trying to connect to database",
                exception=str(repr(e))
               )

# Try generic select endpoint \w pagination & default row limit for lazy loading
# may not really be the best idea for this table, as preloading will make everything more responsive, but good
# to try and use as an example later
@jsonp
def selectChangelogRows():
    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")
    
    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )

    page_arg = request.args.get('page')
    size_arg = request.args.get('size')
    #sorters_arg = request.args.get('sorters')
    filters_0_field = request.args.get('filters[0][field]')
    filters_0_value = request.args.get('filters[0][value]')
    filters_1_field = request.args.get('filters[1][field]')
    filters_1_value = request.args.get('filters[1][value]')
    filters_2_field = request.args.get('filters[2][field]')
    filters_2_value = request.args.get('filters[2][value]')
    filters_3_field = request.args.get('filters[3][field]')
    filters_3_value = request.args.get('filters[3][value]')
    filters_4_field = request.args.get('filters[4][field]')
    filters_4_value = request.args.get('filters[4][value]')
    filters_5_field = request.args.get('filters[5][field]')
    filters_5_value = request.args.get('filters[5][value]')
    filters_6_field = request.args.get('filters[6][field]')
    filters_6_value = request.args.get('filters[6][value]')
    filters_7_field = request.args.get('filters[7][field]')
    filters_7_value = request.args.get('filters[7][value]')
    filters_8_field = request.args.get('filters[8][field]')
    filters_8_value = request.args.get('filters[8][value]')
    filters_9_field = request.args.get('filters[9][field]')
    filters_9_value = request.args.get('filters[9][value]')
    filters_10_field = request.args.get('filters[10][field]')
    filters_10_value = request.args.get('filters[10][value]')

    sql_filters = {}
    if filters_0_field:
        sql_filters[filters_0_field] = filters_0_value
    if filters_1_field:
        sql_filters[filters_1_field] = filters_1_value
    if filters_2_field:
        sql_filters[filters_2_field] = filters_2_value
    if filters_3_field:
        sql_filters[filters_3_field] = filters_3_value
    if filters_4_field:
        sql_filters[filters_4_field] = filters_4_value
    if filters_5_field:
        sql_filters[filters_5_field] = filters_5_value
    if filters_6_field:
        sql_filters[filters_6_field] = filters_6_value
    if filters_7_field:
        sql_filters[filters_7_field] = filters_7_value
    if filters_8_field:
        sql_filters[filters_8_field] = filters_8_value
    if filters_9_field:
        sql_filters[filters_9_field] = filters_9_value
    if filters_10_field:
        sql_filters[filters_10_field] = filters_10_value
    
    #print("sql_filters: ")
    #print(str(sql_filters))

    try:
        with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                           user=config['database_username'], password=config['database_password']) as conn:
            with conn.cursor() as cur:
                # In order to return the mandatory "last_page" data for lazy-loading, we check and see if page and size were request
                # arguments, and do a select COUNT(hospital_key) for total table rows
                if size_arg and page_arg:
                    sql = "SELECT COUNT(changelog_key) FROM " + config['database_name'] + ".dbo.changelog "
                    if len(sql_filters) == 0:
                        pass
                    else:
                        sql = sql + "WHERE "
                        for sql_filter_field, sql_filter_value in sql_filters.items():
                            sql = sql + sql_filter_field + " LIKE '%" + sql_filter_value.replace("'", "''") + "%' AND "
                        if sql[-4:] == "AND ":
                            sql = sql[:-4]
                    #print("SELECT COUNT(changelog_key)")
                    #print(sql)

                    cur.execute(sql)
                    allfetchedrows = cur.fetchall()
                    
                    #print(allfetchedrows[0][0])
                    total_rows = allfetchedrows[0][0]
                    last_page = math.ceil(float(total_rows) / float(size_arg))
                else:
                    last_page = 1

                sql = "SELECT "
                if not size_arg and not page_arg:
                    sql = sql + "TOP 100 "
                sql = sql + "changelog_key, old_pc_id, new_pc_id, old_printer, new_printer, domain, environment, notes, created, createdby, createdby_host, log_entry "
                sql = sql + "FROM " + config['database_name'] + ".dbo.changelog "
                if len(sql_filters) == 0:
                        pass
                else:
                    sql = sql + "WHERE "
                    for sql_filter_field, sql_filter_value in sql_filters.items():
                        sql = sql + sql_filter_field + " LIKE '%" + sql_filter_value.replace("'", "''") + "%' AND "
                    if sql[-4:] == "AND ":
                        sql = sql[:-4]
                sql = sql + "ORDER BY changelog_key DESC "
                if size_arg and page_arg:
                    sql = sql + "OFFSET " + str(int(size_arg) * (int(page_arg) - 1)) + " ROWS "
                    sql = sql + "FETCH NEXT " + str(int(size_arg)) + " ROWS ONLY;"
                else:
                    sql = sql + ";"
                #print(sql)
                cur.execute(sql)
                allfetchedrows = cur.fetchall()
                rows = []
                for row in allfetchedrows:
                    if row[0]:
                        changelog_key = row[0]
                    else:
                        changelog_key = None
                    if row[1]:
                        old_pc_id = row[1].strip()
                    else:
                        old_pc_id = None
                    if row[2]:
                        new_pc_id = row[2].strip()
                    else:
                        new_pc_id = None
                    if row[3]:
                        old_printer = row[3].strip()
                    else:
                        old_printer = None
                    if row[4]:
                        new_printer = row[4]
                    else:
                        new_printer = None
                    if row[5]:
                        domain = row[5].strip()
                    else:
                        domain = None
                    if row[6]:
                        environment = row[6]
                    else:
                        environment = None
                    if row[7]:
                        notes = row[7].strip()
                    else:
                        notes = None
                    if row[8]:
                        created = row[8].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        created = None
                    if row[9]:
                        createdby = row[9].strip()
                    else:
                        createdby = None
                    if row[10]:
                        createdby_host = row[10].strip()
                    else:
                        createdby_host = None
                    if row[11]:
                        log_entry = row[11].strip()
                    else:
                        log_entry = None
                    rows.append({'id':changelog_key,
                                 'changelog_key':changelog_key,
                                 'log_entry':log_entry,
                                 'old_pc_id':old_pc_id,
                                 'new_pc_id':new_pc_id,
                                 'old_printer':old_printer,
                                 'new_printer':new_printer,
                                 'domain':domain,
                                 'environment':environment,
                                 'notes':notes,
                                 'created':created,
                                 'createdby':createdby,
                                 'createdby_host':createdby_host})
                #print(rows)
                return jsonify(success=True,
                               data=rows,
                               last_page=last_page)

    except Exception as e:
        jsonify(success=False,
                   last_page=1,
                   data=[],
                   error=str(e))

    return jsonify(success=True,
                   last_page=1,
                   data=[])

@jsonp
def selectOneHospitalRow():
    
    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )
    
    pc_id_arg = request.args.get('pc_id')
    hospital_key_arg = request.args.get('hospital_key')
    
    if not pc_id_arg and not hospital_key_arg:
        return jsonify(success=False,
                       error="To query for one row, you must include either 'pc_id' request argument or 'hospital_key' argument (or both)")


    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")

    try:
        with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                           user=config['database_username'], password=config['database_password']) as conn:
            with conn.cursor() as cur:
                sql = "SELECT hospital_key, pc_id, printer, notes, created, createdby, edited, editedby, inactivated, inactivatedby FROM " + config['database_name'] + ".dbo.hospital"
                if (pc_id_arg) and (hospital_key_arg):
                    sql = sql + " WHERE pc_id = '" + pc_id_arg + "' AND hospital_key = '" + hospital_key_arg + "';"
                elif (hospital_key_arg):
                    sql = sql + " WHERE hospital_key = '" + hospital_key_arg + "';"
                elif (pc_id_arg):
                    sql = sql + " WHERE pc_id = '" + pc_id_arg + "';"
                else:
                    sql = sql + ';'
                
                #print(sql)
                cur.execute(sql)
                allfetchedrows = cur.fetchall()
                rows = []
                for row in allfetchedrows:
                    if row[0]:
                        hospital_key = row[0]
                    else:
                        hospital_key = None
                    if row[1]:
                        pc_id = row[1].strip()
                    else:
                        pc_id = None
                    if row[2]:
                        printer = row[2].strip()
                    else:
                        printer = None
                    if row[3]:
                        notes = row[3].strip()
                    else:
                        notes = None
                    if row[4]:
                        created = row[4].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        created = None
                    if row[5]:
                        createdby = row[5].strip()
                    else:
                        createdby = None
                    if row[6]:
                        edited = row[6].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        edited = None
                    if row[7]:
                        editedby = row[7].strip()
                    else:
                        editedby = None
                    if row[8]:
                        inactivated = row[8].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        inactivated = None
                    if row[9]:
                        inactivatedby = row[9].strip()
                    else:
                        inactivatedby = None

                    rows.append({'id':hospital_key,
                                 'hospital_key':hospital_key,
                                 'pc_id':pc_id,
                                 'printer':printer,
                                 'notes':notes,
                                 'created':created,
                                 'createdby':createdby,
                                 'edited':edited,
                                 'editedby':editedby,
                                 'inactivated':inactivated,
                                 'inactivatedby':inactivatedby})

                return jsonify(success=True,
                               data=rows)

    except Exception as e:
        return jsonify(success=False,
                error="Error trying to connect to database",
                exception=str(repr(e))
               )

#@app.route("/addOrUpdateOneHospitalRow", methods=['GET'])
@jsonp
def addOrUpdateOneHospitalRow():

    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")

    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )

    # dbo.hospital table columns
    hospital__hospital_key__arg = request.args.get('hospital_key')
    hospital__pc_id__arg = request.args.get('pc_id')
    hospital__printer__arg = request.args.get('printer')
    hospital__notes__arg = request.args.get('notes')
    #hospital__created__arg = request.args.get('created')
    hospital__createdby__arg = request.args.get('createdby')
    #hospital__edited__arg = request.args.get('edited')
    hospital__editedby__arg = request.args.get('editedby')
    hospital__inactivated__arg = request.args.get('inactivated')
    hospital__inactivatedby__arg = request.args.get('inactivatedby')

    # Some error checks
    if not hospital__pc_id__arg and not hospital__printer__arg and not hospital__notes__arg \
       and not hospital__createdby__arg and not hospital__editedby__arg \
       and not hospital__inactivated__arg and not hospital__inactivatedby__arg:
       return jsonify(success=False,
                      error="Error, need to include at least one hospital table column to update.",
                      available_arguments="hospital_key, pc_id, printer, notes, created, createdby, edited, editedby, inactivated, inactivatedby")

    # Create SQL compatible vars for each column, accounting for nulls and single quotes
    hospital__pc_id__sqlarg = (("'" + hospital__pc_id__arg.replace("'", "''") + "'") if hospital__pc_id__arg else "")
    hospital__pc_id__sqlarg = ("NULL" if hospital__pc_id__sqlarg.lower() == "'null'" else hospital__pc_id__sqlarg)
    hospital__printer__sqlarg = (("'" + hospital__printer__arg.replace("'", "''") + "'") if hospital__printer__arg else "")
    hospital__printer__sqlarg = ("NULL" if hospital__printer__sqlarg.lower() == "'null'" else hospital__printer__sqlarg)
    hospital__notes__sqlarg = (("'" + hospital__notes__arg.replace("'", "''") + "'") if hospital__notes__arg else "")
    hospital__notes__sqlarg = ("NULL" if hospital__notes__sqlarg.lower() == "'null'" else hospital__notes__sqlarg)
    #hospital__created__sqlarg = (("'" + hospital__created__arg.replace("'", "''") + "'") if hospital__created__arg else "")
    #hospital__created__sqlarg = ("NULL" if hospital__created__sqlarg.lower() == "'null'" else hospital__created__sqlarg)
    hospital__createdby__sqlarg = (("'" + hospital__createdby__arg.replace("'", "''") + "'") if hospital__createdby__arg else "")
    hospital__createdby__sqlarg = ("NULL" if hospital__createdby__sqlarg.lower() == "'null'" else hospital__createdby__sqlarg)  
    #hospital__edited__sqlarg = (("'" + hospital__edited__arg.replace("'", "''") + "'") if hospital__edited__arg else "")
    #hospital__edited__sqlarg = ("NULL" if hospital__edited__sqlarg.lower() == "'null'" else hospital__edited__sqlarg)
    hospital__editedby__sqlarg = (("'" + hospital__editedby__arg.replace("'", "''") + "'") if hospital__editedby__arg else "")
    hospital__editedby__sqlarg = ("NULL" if hospital__editedby__sqlarg.lower() == "'null'" else hospital__editedby__sqlarg) 
    hospital__inactivated__sqlarg = (("'" + hospital__inactivated__arg.replace("'", "''") + "'") if hospital__inactivated__arg else "")
    hospital__inactivated__sqlarg = ("NULL" if hospital__inactivated__sqlarg.lower() == "'null'" else hospital__inactivated__sqlarg) 
    hospital__inactivatedby__sqlarg = (("'" + hospital__inactivatedby__arg.replace("'", "''") + "'") if hospital__inactivatedby__arg else "")
    hospital__inactivatedby__sqlarg = ("NULL" if hospital__inactivatedby__sqlarg.lower() == "'null'" else hospital__inactivatedby__sqlarg)

    # Check if hospital_key included as a request arg - if so try SQL UPDATE, else do an INSERT
    if hospital__hospital_key__arg:
        try:
            with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                            user=config['database_username'], password=config['database_password']) as conn:
                with conn.cursor() as cur:
                    # Verify the hospital_key exists in the db
                    sql = "SELECT hospital_key FROM " + config['database_name'] + ".dbo.hospital"
                    sql = sql + " WHERE hospital_key = '" + hospital__hospital_key__arg + "';"
                    #print(sql)
                    cur.execute(sql)
                    rows = cur.fetchall()
                    #print(str(rows))
                    if len(rows) < 1:
                        return jsonify(success=False,
                                       error=("Error, hospital_key " + hospital__hospital_key__arg + " does not exist in " + config['database_name'] + ".dbo.hospital"))

                    sql = "UPDATE " + config['database_name'] + ".dbo.hospital SET "
                    sql = ((sql + "pc_id = " + hospital__pc_id__sqlarg + ", ") if hospital__pc_id__arg else sql)
                    sql = ((sql + "printer = " + hospital__printer__sqlarg + ", ") if hospital__printer__arg else sql)
                    sql = ((sql + "notes = " + hospital__notes__sqlarg + ", ") if hospital__notes__arg else sql)
                    #sql = ((sql + "created = " + hospital__created__sqlarg + ", ") if hospital__created__arg else sql)
                    sql = ((sql + "createdby = " + hospital__createdby__sqlarg + ", ") if hospital__createdby__arg else sql)
                    #sql = ((sql + "edited = " + hospital__edited__sqlarg + ", ") if hospital__edited__arg else sql)
                    sql = sql + "edited = CURRENT_TIMESTAMP, "
                    sql = ((sql + "editedby = " + hospital__editedby__sqlarg + ", ") if hospital__editedby__arg else sql)
                    sql = ((sql + "inactivated = " + hospital__inactivated__sqlarg + ", ") if hospital__inactivated__arg else sql)
                    sql = ((sql + "inactivatedby = " + hospital__inactivatedby__sqlarg + ", ") if hospital__inactivatedby__arg else sql)
                    sql = sql[:-2]
                    sql = sql + " WHERE "
                    sql = sql + "hospital_key = '" + hospital__hospital_key__arg + "'"
                    #print(sql)
                    cur.execute(sql)
                    conn.commit()
                    return jsonify(success=True,
                                   new_row=False,
                                   sql=sql
                                  )
        except Exception as e:
            return jsonify(success=False,
                    error="Error trying to connect/update database",
                    exception=str(repr(e))
                )
    # If hospital_key is not specified, we insert a new row
    else: 
        try:
            with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                            user=config['database_username'], password=config['database_password']) as conn:
                with conn.cursor() as cur:
                    sql = "INSERT INTO " + config['database_name'] + ".dbo.hospital "
                    sql = sql + "(pc_id, printer, notes, created, createdby, edited, editedby, inactivated, inactivatedby) "
                    sql = sql + "VALUES ("
                    sql = ((sql + hospital__pc_id__sqlarg + ", ") if hospital__pc_id__arg else (sql + "NULL, "))
                    sql = ((sql + hospital__printer__sqlarg + ", ") if hospital__printer__arg else (sql + "NULL, "))
                    sql = ((sql + hospital__notes__sqlarg + ", ") if hospital__notes__arg else (sql + "NULL, "))
                    #sql = ((sql + hospital__created__sqlarg + ", ") if hospital__created__arg else (sql + "NULL, "))
                    sql = sql + "CURRENT_TIMESTAMP, "
                    sql = ((sql + hospital__createdby__sqlarg + ", ") if hospital__createdby__arg else (sql + "NULL, "))
                    #sql = ((sql + hospital__edited__sqlarg + ", ") if hospital__edited__arg else (sql + "NULL, "))
                    sql = sql + "NULL, "
                    sql = ((sql + hospital__editedby__sqlarg + ", ") if hospital__editedby__arg else (sql + "NULL, "))
                    sql = ((sql + hospital__inactivated__sqlarg + ", ") if hospital__inactivated__arg else (sql + "NULL, "))
                    sql = ((sql + hospital__inactivatedby__sqlarg + ", ") if hospital__inactivatedby__arg else (sql + "NULL, "))
                    sql = sql[:-2]
                    sql = sql + ")"
                    #print(sql)
                    cur.execute(sql)
                    conn.commit()
                    return jsonify(success=True,
                                   new_row=True,
                                   sql=sql
                                  )
        except Exception as e:
            return jsonify(success=False,
                    error="Error trying to connect/insert database",
                    exception=str(repr(e))
                )

@jsonp
def deleteOneHospitalRow():
    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")

    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )

    # dbo.hospital table columns
    hospital__hospital_key__arg = request.args.get('hospital_key')

    # Make sure API has the hospital_key to identify the row to delete
    if not hospital__hospital_key__arg:
        return jsonify(success=False,
                      error="Error, need to include hospital_key argument.",
                      available_arguments="hospital_key")
    try:
        with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                        user=config['database_username'], password=config['database_password']) as conn:
            with conn.cursor() as cur:
                # Verify the hospital_key exists in the db
                sql = "SELECT hospital_key FROM " + config['database_name'] + ".dbo.hospital"
                sql = sql + " WHERE hospital_key = '" + hospital__hospital_key__arg + "';"
                #print(sql)
                cur.execute(sql)
                rows = cur.fetchall()
                #print(str(rows))
                if len(rows) < 1:
                    return jsonify(success=False,
                                    error=("Error, hospital_key " + hospital__hospital_key__arg + " does not exist in " + config['database_name'] + ".dbo.hospital"))

                # Perform the dele
                sql = "DELETE FROM " + config['database_name'] + ".dbo.hospital"
                sql = sql + " WHERE "
                sql = sql + "hospital_key = '" + hospital__hospital_key__arg + "'"
                #print(sql)
                cur.execute(sql)
                conn.commit()
                return jsonify(success=True,
                                sql=sql
                                )
    except Exception as e:
        return jsonify(success=False,
                error="Error trying to connect/delete row in database",
                exception=str(repr(e))
            )
    

@jsonp
def addOneChangelogRow():
    config = loadConfigFile()
    if ('error' in config):
        return jsonify(success=False,
            config="Error Loading Config file")

    # API endpoints are secured with passkey, check this first
    passkey = request.args.get('passkey')
    samAccountName = request.args.get('samAccountName')
    domain = request.args.get('domain')
    if not passkey or not samAccountName or not domain:
        return jsonify(success=False,
                error="Valid 'samAccountName', 'domain', and 'passkey' request arguments must be passed to access this API."
               )
    if not query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
        return jsonify(success=False,
                error="One or more request arguments: 'samAccountName', 'domain', and 'passkey' were not valid."
               )
               
    # dbo.hospital table columns
    changelog__log_entry__arg = request.args.get('log_entry')
    changelog__old_pc_id__arg = request.args.get('old_pc_id')
    changelog__new_pc_id__arg = request.args.get('new_pc_id')
    changelog__old_printer__arg = request.args.get('old_printer')
    changelog__new_printer__arg = request.args.get('new_printer')
    changelog__domain__arg = request.args.get('domain')
    changelog__environment__arg = request.args.get('environment')
    changelog__notes__arg = request.args.get('notes')
    changelog__created__arg = request.args.get('created')
    changelog__createdby__arg = request.args.get('createdby')
    changelog__createdby_host__arg = request.args.get('createdby_host')

    # Create SQL compatible vars for each column, accounting for nulls and single quotes
    changelog__log_entry__sqlarg = (("'" + changelog__log_entry__arg.replace("'", "''")[0:254] + "'") if changelog__log_entry__arg else "")
    changelog__log_entry__sqlarg = ("NULL" if changelog__log_entry__sqlarg.lower() == "'null'" else changelog__log_entry__sqlarg)
    changelog__old_pc_id__sqlarg = (("'" + changelog__old_pc_id__arg.replace("'", "''")[0:254] + "'") if changelog__old_pc_id__arg else "")
    changelog__old_pc_id__sqlarg = ("NULL" if changelog__old_pc_id__sqlarg.lower() == "'null'" else changelog__old_pc_id__sqlarg)
    changelog__new_pc_id__sqlarg = (("'" + changelog__new_pc_id__arg.replace("'", "''")[0:254] + "'") if changelog__new_pc_id__arg else "")
    changelog__new_pc_id__sqlarg = ("NULL" if changelog__new_pc_id__sqlarg.lower() == "'null'" else changelog__new_pc_id__sqlarg)
    changelog__old_printer__sqlarg = (("'" + changelog__old_printer__arg.replace("'", "''")[0:254] + "'") if changelog__old_printer__arg else "")
    changelog__old_printer__sqlarg = ("NULL" if changelog__old_printer__sqlarg.lower() == "'null'" else changelog__old_printer__sqlarg)
    changelog__new_printer__sqlarg = (("'" + changelog__new_printer__arg.replace("'", "''")[0:254] + "'") if changelog__new_printer__arg else "")
    changelog__new_printer__sqlarg = ("NULL" if changelog__new_printer__sqlarg.lower() == "'null'" else changelog__new_printer__sqlarg)
    changelog__domain__sqlarg = (("'" + changelog__domain__arg.replace("'", "''")[0:254] + "'") if changelog__domain__arg else "")
    changelog__domain__sqlarg = ("NULL" if changelog__domain__sqlarg.lower() == "'null'" else changelog__domain__sqlarg)
    changelog__environment__sqlarg = (("'" + changelog__environment__arg.replace("'", "''")[0:127] + "'") if changelog__environment__arg else "")
    changelog__environment__sqlarg = ("NULL" if changelog__environment__sqlarg.lower() == "'null'" else changelog__environment__sqlarg)
    changelog__notes__sqlarg = (("'" + changelog__notes__arg.replace("'", "''")[0:254] + "'") if changelog__notes__arg else "")
    changelog__notes__sqlarg = ("NULL" if changelog__notes__sqlarg.lower() == "'null'" else changelog__notes__sqlarg)
    #changelog__created__sqlarg = (("'" + changelog__created__arg.replace("'", "''") + "'") if changelog__created__arg else "")
    #changelog__created__sqlarg = ("NULL" if changelog__created__sqlarg.lower() == "'null'" else changelog__created__sqlarg)
    changelog__createdby__sqlarg = (("'" + changelog__createdby__arg.replace("'", "''")[0:127] + "'") if changelog__createdby__arg else "")
    changelog__createdby__sqlarg = ("NULL" if changelog__createdby__sqlarg.lower() == "'null'" else changelog__createdby__sqlarg)
    changelog__createdby_host__sqlarg = (("'" + changelog__createdby_host__arg.replace("'", "''")[0:254] + "'") if changelog__createdby_host__arg else "")
    changelog__createdby_host__sqlarg = ("NULL" if changelog__createdby_host__sqlarg.lower() == "'null'" else changelog__createdby_host__sqlarg)
    
    try:
        with pytds.connect(server=config['database_hostname'], database=config['database_name'],
                        user=config['database_username'], password=config['database_password']) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO " + config['database_name'] + ".dbo.changelog "
                sql = sql + "(log_entry, old_pc_id, new_pc_id, old_printer, new_printer, domain, environment, notes, created, createdby, createdby_host) "
                sql = sql + "VALUES ("
                sql = ((sql + changelog__log_entry__sqlarg + ", ") if changelog__log_entry__arg else (sql + "NULL, "))
                sql = ((sql + changelog__old_pc_id__sqlarg + ", ") if changelog__old_pc_id__arg else (sql + "NULL, "))
                sql = ((sql + changelog__new_pc_id__sqlarg + ", ") if changelog__new_pc_id__arg else (sql + "NULL, "))
                sql = ((sql + changelog__old_printer__sqlarg + ", ") if changelog__old_printer__arg else (sql + "NULL, "))
                sql = ((sql + changelog__new_printer__sqlarg + ", ") if changelog__new_printer__arg else (sql + "NULL, "))
                sql = ((sql + changelog__domain__sqlarg + ", ") if changelog__domain__arg else (sql + "NULL, "))
                sql = ((sql + changelog__environment__sqlarg + ", ") if changelog__environment__arg else (sql + "NULL, "))
                sql = ((sql + changelog__notes__sqlarg + ", ") if changelog__notes__arg else (sql + "NULL, "))
                sql = sql + "CURRENT_TIMESTAMP, "
                sql = ((sql + changelog__createdby__sqlarg + ", ") if changelog__createdby__arg else (sql + "NULL, "))
                sql = ((sql + changelog__createdby_host__sqlarg + ", ") if changelog__createdby_host__arg else (sql + "NULL, "))
                sql = sql[:-2]
                sql = sql + ")"
                #print(sql)
                cur.execute(sql)
                conn.commit()
                return jsonify(success=True,
                                new_row=True,
                                sql=sql
                                )
    except Exception as e:
        return jsonify(success=False,
                error="Error trying to connect/insert database",
                exception=str(repr(e))
            )

    return jsonify(success=False,
                   new_row=True
                  )

    