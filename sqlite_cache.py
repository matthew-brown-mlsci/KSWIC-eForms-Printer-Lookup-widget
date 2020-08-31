"""

KSWIC eForms Printer Lookup service

"""

import os
from os.path import exists
import time
import datetime
from functools import wraps
import tempfile
import sqlite3

from random import seed
from random import randint

from kswic_objs import *
from kswic_config import *

def create_sqlite_cache_if_not_exist(fn):
    try:
        # Check to see if sqlite file exists, if it does not, create one
        print(fn)
        if not exists(fn):
            log_entry("SQLite cache db not found, creating " + fn)
            
            conn = sqlite3.connect(fn)
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE ad_cache
                        (domain text, samAccountName text, passkey text, timestamp text, access_level text, access_from_user_or_group text, ad_resource text)''')
            # Save (commit) the changes
            conn.commit()
            conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def query_sqlite_cache_one_row(domain, samAccountName):
    #tmpdir = tempfile.gettempdir()
    #fn = tmpdir + '\\' + sqlite_cache_file
    fn = sqlite_cache_file
    conn = sqlite3.connect(fn)
    c = conn.cursor()
    # search for user/domain
    sql = "SELECT samAccountName, domain, passkey, timestamp, access_level, access_from_user_or_group, ad_resource \
                FROM ad_cache \
                WHERE samAccountName = '" + str(samAccountName) + "' " + \
                "AND domain = '" + str(domain) + "' AND \
                timestamp > datetime('now', '-1 day') AND \
                access_level != 'None'"
    #print(sql)

    c.execute(sql)
    cached_record = c.fetchone()
    c.close()
    conn.close()
    return cached_record

def query_sqlite_cache_verify_passkey(domain, samAccountName, passkey):
    #tmpdir = tempfile.gettempdir()
    #fn = tmpdir + '\\' + sqlite_cache_file
    fn = sqlite_cache_file
    conn = sqlite3.connect(fn)
    c = conn.cursor()
    # search for user/domain
    sql = "SELECT samAccountName, domain, passkey, timestamp, access_level, access_from_user_or_group, ad_resource \
                FROM ad_cache \
                WHERE samAccountName = '" + str(samAccountName) + "' " + \
                "AND domain = '" + str(domain) + "' AND \
                timestamp > datetime('now', '-1 day') AND \
                access_level != 'None'"
    #print(sql)

    c.execute(sql)
    cached_record = c.fetchone()
    c.close()
    conn.close()
    #print(cached_record)
    valid_passkey = cached_record[2]
    if passkey == valid_passkey:
        return True
    else:
        return False

def query_sqlite_cache_replace_row(samAccountName, domain, access_level, access_from_user_or_group, ad_resource):

    seed(1)
    new_passkey = randint(0, 9999999999999)

    #tmpdir = tempfile.gettempdir()
    #fn = tmpdir + '\\' + sqlite_cache_file
    fn = sqlite_cache_file
    conn = sqlite3.connect(fn)
    c = conn.cursor()
    
    if not access_level:
        access_level = "NULL"
    else:
        access_level = "'" + str(access_level) + "'"

    if not access_from_user_or_group:
        access_from_user_or_group = "NULL"
    else:
        access_from_user_or_group = "'" + str(access_from_user_or_group) + "'"

    if not ad_resource:
        ad_resource = "NULL"
    else:
        ad_resource = "'" + str(ad_resource) + "'"

    sql = "INSERT INTO ad_cache (samAccountName, domain, passkey, timestamp, access_level, access_from_user_or_group, ad_resource) \
           SELECT '" + str(samAccountName) + "', '" + str(domain) + "', '" + str(new_passkey) + "', datetime('now'), " +  str(access_level) + ", \
           " + str(access_from_user_or_group) + ", " + str(ad_resource) + " \
           WHERE NOT EXISTS (SELECT 1 FROM ad_cache WHERE samAccountName='" + str(samAccountName) + "' AND domain='" + str(domain) + "');"
    #print(sql)
    c.execute(sql)
    conn.commit()

    sql = "UPDATE ad_cache SET timestamp = datetime('now'), passkey = '" + str(new_passkey) + "' WHERE samAccountName='" + str(samAccountName) + "' AND domain='" + str(domain) + "';"
    c.execute(sql)
    conn.commit()
    #print(sql)
    c.close()
    conn.close()
    return


