"""

Test service to run a website that allows users in a certain AD group 
to access/update the sqprod6 Printer_Lookup db

"""

from flask import Flask, send_from_directory, render_template
import sys
import os
import time
import datetime
from flask import jsonify
import socket
from flask import redirect, request, current_app, app

import base64
import struct

from kswic_objs import *
from kswic_config import *
import kswic_api
import kswic_misc
import active_directory

hostname = socket.gethostname()
app = Flask(__name__)

app.add_url_rule('/fakeWinAuthInfo', view_func=kswic_misc.fakeWinAuthInfo)
#app.add_url_rule('/ListRoutes', view_func=kswic_misc.ListRoutes)
app.add_url_rule('/getWinAuthInfo', view_func=kswic_misc.getWinAuthInfo)

app.add_url_rule('/verifyUserAccess', view_func=active_directory.verifyUserAccess)
app.add_url_rule('/ListKnownDomains', view_func=active_directory.ListKnownDomains)
app.add_url_rule('/GroupUsers', view_func=active_directory.GroupUsers)

app.add_url_rule('/selectAllHospitalRows', view_func=kswic_api.selectAllHospitalRows)
app.add_url_rule('/selectChangelogRows', view_func=kswic_api.selectChangelogRows)
app.add_url_rule('/selectOneHospitalRow', view_func=kswic_api.selectOneHospitalRow)
app.add_url_rule('/addOrUpdateOneHospitalRow', view_func=kswic_api.addOrUpdateOneHospitalRow)
app.add_url_rule('/deleteOneHospitalRow', view_func=kswic_api.deleteOneHospitalRow)
app.add_url_rule('/addOneChangelogRow', view_func=kswic_api.addOneChangelogRow)

@app.route("/", methods=['GET'])
def spareIndex():
    return render_template('index.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('frontend/src', path)

@app.route("/ListRoutes", methods=['GET'])
@jsonp
def ListRoutes():
    routes = []

    for rule in app.url_map.iter_rules():
        routes.append('%s' % rule)

    return jsonify(success=True,
                   routes=[e for e in routes])

@app.route("/config_files", methods=['GET'])
@jsonp
def config_files():
    return jsonify(success=True,
                   logfile = logfile,
                   config_file = config_file,
                   ad_file = ad_file,
                   domain_config_file = domain_config_file,
                   sqlite_cache_file = sqlite_cache_file
                   )

if __name__ == "__main__":
    #app.run(ssl_context='adhoc', debug=True, host='0.0.0.0', port=9990)
    app.run(debug=True, host='0.0.0.0', port=port)