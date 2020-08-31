"""

KSWIC eForms Printer Lookup config py

"""

from functools import wraps
from flask import request
import socket
from flask import Flask
from kswic_objs import *
#from __main__ import app
import datetime
import os
import sys

port = 9980
logfile = "KSWIC eForms Printer Lookup service log.txt"
config_file = "KSWIC eForms Printer Lookup service config.txt"
ad_file = "KSWIC eForms Printer Lookup service AD groups and users.txt"
domain_config_file = "domains.txt"
sqlite_cache_file = "KSWIC eForms Printer Lookup service.db"
frontend_config_js = "frontend\\src\\config.js"

# Fix path if running as a windows service
if sys.executable:
    if sys.executable.split('\\')[-1] == 'python.exe':
        # We're running locally in a dev env!
        local_dir = str(os.getcwd())
        logfile = local_dir + "\\" + logfile
        config_file = local_dir + "\\" + config_file
        ad_file = local_dir + "\\" + ad_file
        domain_config_file = local_dir + "\\" + domain_config_file
        sqlite_cache_file = local_dir + "\\" + sqlite_cache_file
        frontend_config_js = local_dir + "\\" + frontend_config_js
    else:
        # Must be in a windows service!
        service_installed_dir = str(os.path.dirname(sys.executable))
        logfile = service_installed_dir + "\\" + logfile
        config_file = service_installed_dir + "\\" + config_file
        ad_file = service_installed_dir + "\\" + ad_file
        domain_config_file = service_installed_dir + "\\" + domain_config_file
        sqlite_cache_file = service_installed_dir + "\\" + sqlite_cache_file
        frontend_config_js = service_installed_dir + "\\" + frontend_config_js

# Wrapper functions to support JSONP requests should we want to access this API from a browser in the future
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            resp = func(*args, **kwargs)
            resp.set_data('{}({})'.format(
                str(callback),
                resp.get_data(as_text=True)
            ))
            resp.mimetype = 'application/javascript'
            return resp
        else:
            return func(*args, **kwargs)
    return decorated_function

# Load config file, returns dict of params
def loadConfigFile():
    config_dict = {}
    allowed_ad_groups = []
    allowed_ad_users = []
    try:
        with open(config_file, 'r') as f:
            line = f.readline()
            while line:
                if ('database|' in line):
                    config_dict['database_name'] = line.split('|')[1]
                    config_dict['database_hostname'] = line.split('|')[2]
                    config_dict['database_username'] = line.split('|')[3]
                    config_dict['database_password'] = line.split('|')[4].strip()
                if ('ad_group|' in line):
                    allowed_ad_groups.append({"domain":line.split('|')[1],
                                              "ad_group":line.split('|')[2],
                                              "access_level":line.split('|')[3].strip()})
                if ('ad_user|' in line):
                    allowed_ad_users.append({"domain":line.split('|')[1],
                                              "ad_user":line.split('|')[2],
                                              "access_level":line.split('|')[3].strip()})
                line = f.readline()
            config_dict['allowed_ad_groups'] = allowed_ad_groups
            config_dict['allowed_ad_users'] = allowed_ad_users

    except Exception as e:
        return({'error':'Error opening or reading ' + config_file, 'exception':str(e)})
    return config_dict


# Add a log entry + datetime
def log_entry(log_message):
	with open(logfile, 'a') as f:
		f.write(str(datetime.datetime.now()) + " : ")
		f.write(log_message + '\n')
