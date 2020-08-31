# KSWIC-eForms-Printer-Lookup-widget
Combines a web front-end with an API for allowing active directory controlled access to modifed/update a SQL db - all encapsulated in a windows python/flask service.  Web front end uses webpack (via docker) to compile javascript to bundles (es5/6 polymorph ie/chrome/firefox compatible!).  The API/web server is configured to sit behind an IIS reverse proxy such that NTLM auth username headers can
be captured and used to facilitate pass-through active directory authentication.

End product - website that desktop pc support staff can use to update an application-specific database.  This removes the burden of 
list maintenance from the Cerner / Access eForms application teams and allows the techs in the field swapping PC's to quickly 
update printing locale information, while only allowing logged/limited database access via a friendly web front end (React based, uses 
React-Tabulator for searchable/sortable tables).

!(https://github.com/matthew-brown-mlsci/KSWIC-eForms-Printer-Lookup-widget/blob/master/screencap1.jpg)
!(https://github.com/matthew-brown-mlsci/KSWIC-eForms-Printer-Lookup-widget/blob/master/screencap2.jpg)

# Install dependencies (build done on Win10 x64 env)
Install WinPython x64\
(Winpython x64 cmd as admin)\
pip install -r requirements.txt\
pip install pyinstaller\
\
Install docker desktop\
(cmd as admin)\
docker pull jmfirth/webpack\
\
Install gitbash for windows\
(from gitbash cmd prompt, cd to desired repo location)\
git clone git@github.ascension.org:A78808/KSWIC-eForms-Printer-Lookup-widget.git\
\
Install NPM dependencies and use webpack to build prod js bundle\
(cmd as admin)\
docker run --rm -i -t -v /c/repo-folder-of-your-choice/KSWIC-eForms-Printer-Lookup-widget/frontend/src:/app jmfirth/webpack npm install --no-bin-links\
docker run --rm -i -t -v /c/repo-folder-of-your-choice/KSWIC-eForms-Printer-Lookup-widget/frontend/src:/app -p 3000:8080 jmfirth/webpack webpack -p --no-bin-links\
\
(verify frontend/src/browser-bundle.js has a nice new timestamp)\
\
(run WinPython x64 cmd as admin)\
c:\
cd repo-folder-of-your-choice\KSWIC-eForms-Printer-Lookup-widget\
mkdir service_build \
copy /y *.py service_build \
mkdir service_build\frontend \
mkdir service_build\frontend\src \
mkdir service_build\frontend\src\react-tabulator \
mkdir service_build\templates \
copy /y templates\* service_build\templates \
copy /y frontend\src\browser-bundle.js service_build\frontend\src \
copy /y frontend\src\fancy.css service_build\frontend\src \
copy /y frontend\src\index.html service_build\frontend\src \
copy /y frontend\src\react-tabulator\* service_build\frontend\src\react-tabulator \
set PYTHONHOME=C:\aisdev\python37\python-3.7.1.amd64\ \
set PYTHONPATH=C:\aisdev\python37\python-3.7.1.amd64\Lib\ \
cd service_build \
pyinstaller -F --add-data "frontend;frontend" --add-data "templates;templates" --hidden-import=win32timezone "KSWIC Eforms Printer Lookup service.py" \
- Use signtool.exe here to add digital signature to "dist\KSWIC Eforms Printer Lookup service.exe" - Ascension Cylance will disable unsigned programs! \
mkdir c:\scripts \
mkdir "c:\scripts\KSWIC Eforms Printer Lookup service" \
copy /y "dist\KSWIC Eforms Printer Lookup service.exe" "c:\scripts\KSWIC Eforms Printer Lookup service\KSWIC Eforms Printer Lookup service.exe" \
cd "c:\scripts\KSWIC Eforms Printer Lookup service" \
"KSWIC Eforms Printer Lookup service.exe" install \

# Service should now be installed, running on port 9980
To use the website/api, an IIS reverse proxy website should be setup to point at localhost:9980 \
- Download and run the Microsoft web platform installer
- Search for Url Rewrite
    - install Url Rewrite + any dependencies
    - restart IIS server
- Create new site 
    - set open binding port etc
    - Authentication
        - disable anonymous
        - enable Windows Authentication
            - click on Windows Authentication
                - Click on Providers 
                - Remove all entries except NTLM 
    - URL Rewrite 
        - Add new rule 
            - Reversey Proxy Inbound rule 
            - Pattern = (.*) 
            - Rewrite URL = http://127.0.0.1:9980/{R:1} 
\
- Restart IIS and connect to site! \
