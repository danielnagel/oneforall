import sys
import requests
from requests_ntlm import HttpNtlmAuth

#  Dateinamen auslesen
fileName = sys.argv[1]

#  SharePoint URL und Ziel Bibliothek
sharePointUrl = 'https://sharepoint.propersonal.de'
folderUrl = '/BZ-Rechner/SiteAssets/BZ-Rechner'

#  Request URL vorbereiten
requestUrl = sharePointUrl + '/_api/web/getfolderbyserverrelativeurl(\'' + folderUrl + '\')/Files/add(url=\'' + fileName + '\',overwrite=true)'

#  Datei lesen
file = open(fileName, 'rb')

#  Header für die Kommunikation mit SharePoint vorbereiten
headers = {'Content-Type': 'application/json; odata=verbose','accept': 'application/json;odata=verbose'}

#  Request ausführen, um das FormDigestValue zu erhalten.
#  Dieser wird gebraucht, um unseren upload zu authentifizieren.
r = requests.post(sharePointUrl + "/_api/contextinfo",
auth=HttpNtlmAuth('domain\\user','password'), headers=headers)
formDigestValue = r.json()['d']['GetContextWebInformation']['FormDigestValue']
print(formDigestValue)

#  Headers um den erhaltenen FormDigestValue aktualisieren.
headers = {'Content-Type': 'application/json; odata=verbose','accept': 'application/json;odata=verbose', 'x-requestdigest' : formDigestValue}

#  Request ausführen.
uploadResult = requests.post(requestUrl, auth=HttpNtlmAuth('domain\\user','password'), headers=headers, data=file.read())
print(uploadResult)
