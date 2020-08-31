"""

    Test service to run a website that allows users in a certain AD group 
to access/update the sqlprod6 Printer_Lookup db

compiling to service + install (in winpython cmd as admin):
        set PYTHONHOME=C:\aisdev\python37\python-3.7.1.amd64\
	    set PYTHONPATH=C:\aisdev\python37\python-3.7.1.amd64\Lib\
        pip install pyinstaller
        
        pyinstaller -F --add-data "frontend;frontend" --add-data "templates;templates" --add-data "static;static" --hidden-import=win32timezone "KSWIC Eforms Printer Lookup service.py"

        mkdir "c:\scripts"
        mkdir "c:\scripts\KSWIC Eforms Printer Lookup service"
        copy "dist\KSWIC Eforms Printer Lookup service.exe" "c:\scripts\KSWIC Eforms Printer Lookup service\KSWIC Eforms Printer Lookup service.exe"
        c:
        cd "c:\scripts\KSWIC Eforms Printer Lookup service"
        "KSWIC Eforms Printer Lookup service.exe" install

    testing:
        curl -s "http://localhost:9990/openfiles"
"""

import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import datetime
from kswic_config import *

from myapp import app

# Add a log entry + datetime
def log_entry(log_message):
	with open(logfile, 'a') as f:
		f.write(str(datetime.datetime.now()) + " : ")
		f.write(log_message + '\n')

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "KSWIC Eforms Printer Lookup service"
    _svc_display_name_ = "KSWIC Eforms Printer Lookup service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(10)

    def SvcStop(self):
        log_entry('SvcStop started')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        log_entry('SvrStop finished')

    def SvcDoRun(self):
        log_entry('SvrDoRun started')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.flaskmain()
        
    def flaskmain(self):
        log_entry('flaskmain() started')
        try:
            app.run(debug=False, host='0.0.0.0', port=port)
        except Exception as e:
            log_entry(str(e))
        log_entry('flaskmain() finished')


if __name__ == '__main__':
    log_entry("KSWIC Eforms Printer Lookup service started")
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FlaskService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FlaskService)
    log_entry("KSWIC Eforms Printer Lookup service stopped")