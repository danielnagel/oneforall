import requests
from requests_ntlm import HttpNtlmAuth
#  import json #print(json.dumps(result.json(), sort_keys=True, indent=4))
#  Beautified eine JSON-Datei
from os.path import join, dirname
from getpass import getpass
import re
import json

username = 'propersonal\\'
username += input("Benutzernamen eingeben: ")
password = getpass("Passwort eingeben: ")
fileName = "test.txt"

#  SharePoint URL und Ziel Bibliothek
sharePointUrl = 'https://sharepoint.propersonal.de'
folderUrl = '/BZ-Rechner/'
#  Request URL vorbereiten
requestUrl = sharePointUrl + folderUrl
serverRelativeUrl = 'SiteAssets/BZ-Rechner'
getFiles = "_api/web/GetFolderByServerRelativeUrl('" + serverRelativeUrl + "')/files"


#  Header für die Kommunikation mit SharePoint vorbereiten
headers = {'Content-Type': 'application/json; odata=verbose',
           'accept': 'application/json;odata=verbose'}

#  Request ausführen, um das FormDigestValue zu erhalten.
#  Dieser wird gebraucht, um unseren upload zu authentifizieren.
result = requests.post(requestUrl + '_api/contextinfo', headers = headers,
                  auth = HttpNtlmAuth(username, password))

print("---")
print("Ergebnis FormDigestValue holen:", result.status_code)
print("---")

formDigestValue = result.json()['d']['GetContextWebInformation']['FormDigestValue']

#  Datei lesen
file = open(join(dirname(__file__), fileName), 'rb')
#  os.path.dirname(__file__) gibt den Pfad zum Python Skript aus

#  Header um den erhaltenen FormDigestValue aktualisieren.
headers = {'Content-Type': 'application/json; odata=verbose',
           'accept': 'application/json;odata=verbose',
           'x-requestdigest': formDigestValue}

#  Datei hochladen
result = requests.post(requestUrl + getFiles +
                       "/add(overwrite=true, url='test.txt')",
                       headers = headers,
                       auth = HttpNtlmAuth(username, password),
                       data=file.read())

print("---")
print("Ergebnis Datei hochladen:", result.status_code)
print("---")

#  Dateien ausgeben
result = requests.post(requestUrl + getFiles, headers = headers,
                       auth = HttpNtlmAuth(username, password))

print("---")
print("Ergebnis Datei ausgeben:", result.status_code)
print("---")

check = re.compile('4..')
if check.match(str(result.status_code)) != None:
    try:
        errMessage = result.json()['error']['message']['value']
        print(errMessage)
    except json.decoder.JSONDecodeError:
        print("Keine valide JSON-Datei!")
        print("Die Datei konnte nicht hochgeladen werden.")
else:
    print(result.status_code)

    files = result.json()['d']['results']
    for file in files:
        print(file['Name'])
