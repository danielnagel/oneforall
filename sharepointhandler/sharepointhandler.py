import requests
import re
import json
from requests_ntlm import HttpNtlmAuth
from os.path import join, exists


def isJSON(string):
    """ Prüft ob eine valide JSON vorliegt.

        :param string: Die zu validierende JSON.
        :return: True bei einer validen JSON, ansonsten False.
    """
    try:
        json.loads(string)
        return True
    except ValueError:
        return False


def isBadRequest(status_code):
    """ Prüft ob ein 4xx HTTP Status Code vorliegt.

        :param status_code: Der zu prüfende HTTP Status Code.
        :return: True wenn ein 4xx HTTP Status Code vorliegt, ansonsten False.
    """
    check = re.compile('4..')
    if check.match(str(status_code)) is not None:
        return True
    else:
        return False


def printReadableJSON(json):
    """ Gibt eine JSON leserlich aus, für Debug Zwecke.

        :param json: Die zu verschönernde JSON.
    """
    print(json.dumps(json.json(), sort_keys=True, indent=4))


def getDigestValue(username, password, requestUrl):
    """ Der Digest Value hat die Funktionsweise eines Cookies.
        Dieser muss bei jeder Anfrage mitgesendet werden, um sich zu
        authentifizieren.

        :param username: Der Benutzername.
        :param password: Das Benutzer Passwort.
        :param requestUrl: Die URL zur SharePoint Webseite bzw. Unterwebseite.
        :return: Digest Value, welcher den Benutzer authentifiziert. Oder None
                 wenn der request fehlgeschlagen ist.
    """
    #  Header für die Kommunikation mit SharePoint vorbereiten
    headers = {'Content-Type': 'application/json; odata=verbose',
               'accept': 'application/json;odata=verbose'}

    #  Request ausführen, um den Digest Value zu erhalten.
    result = requests.post(requestUrl + '_api/contextinfo', headers = headers,
                      auth = HttpNtlmAuth(username, password))

    #  Request Status Code überprüfen
    if isBadRequest(result.status_code):
        print("Anfrage fehlgeschlagen.")
        print("Keinen Digest Value erhalten.")
        return None

    # Digest Value aus der JSON auslesen
    if isJSON(result.content):
        digestValue = result.json()['d']['GetContextWebInformation']['FormDigestValue']
        return digestValue
    else:
        print("Keine valide JSON-Datei!")
        print("Keinen Digest Value erhalten.")
        return None


def uploadFile(username, password, path, fileName, requestUrl,
               serverRelativeUrl, digestValue):
    """ Lädt eine Datei ins SharePoint hoch.

        :param username: Der Benutzername.
        :param password: Das Benutzer Passwort.
        :param path: Pfad zur Datei die hochgeladen werden soll.
        :param fileName: Name der Datei die hochgeladen werden soll.
        :param requestUrl: Die URL zur SharePoint Webseite bzw. Unterwebseite.
        :param serverRelativeUrl: Relativer Serverpfad welcher das Upload
                                  Verzeichnis spezifiziert.
        :param digestValue: Der Digest Value authentifiziert den Benutzer.
        :return: True wenn alles geklappt hat, ansonsten False.
    """
    #  Header zum hochladen der Datei vorbereiten.
    headers = {'Content-Type': 'application/json; odata=verbose',
               'accept': 'application/json;odata=verbose',
               'x-requestdigest': digestValue}

    # Relativer Pfad zum SharePoint Verzeichnis
    getFiles = "_api/web/GetFolderByServerRelativeUrl('" + serverRelativeUrl \
            + "')/files"

    #  Datei lesen
    uploadFile = join(path, fileName)
    if exists(uploadFile):
        try:
            file = open(uploadFile, 'rb')
        except:
            print("Datei '" + uploadFile + "' kann nicht geöffnet werden.")
            return False
    else:
        print("Die Datei '" + uploadFile + "' ist nicht vorhanden!")
        return False


    #  Datei hochladen
    result = requests.post(requestUrl + getFiles +
                           "/add(overwrite=true, url='" + fileName + "')",
                           headers = headers, data=file.read(),
                           auth = HttpNtlmAuth(username, password))

    #  Request Status Code überprüfen
    if isBadRequest(result.status_code):
        print("Anfrage fehlgeschlagen.")
        print("Keine Datei hochgeladen.")
        return False
    else:
        print("Datei erfolgreich hochgeladen.")
        return True


def createFolder(username, password, requestUrl, serverRelativeUrl, newDirName,
                 digestValue):
    """ Erstellt einen noch nicht vorhandenes Verzeichnis im SharePoint.

        :param username: Der Benutzername.
        :param password: Das Benutzer Passwort.
        :param requestUrl: Die URL zur SharePoint Webseite bzw. Unterwebseite.
        :param serverRelativeUrl: Relativer Serverpfad welcher das Upload
                                  Verzeichnis spezifiziert.
        :param newDirName: Der Name des neuen Verzeichnisses.
        :param digestValue: Der Digest Value authentifiziert den Benutzer.
        :return: True wenn alles geklappt hat, ansonsten False.
    """
    #  Header zum hochladen der Datei vorbereiten.
    headers = {'Content-Type': 'application/json; odata=verbose',
               'accept': 'application/json;odata=verbose',
               'x-requestdigest': digestValue}

    # Relativer Pfad zum SharePoint Verzeichnis
    getFolders = "_api/web/Folders/add('" + serverRelativeUrl + newDirName + "')"

    #  Verzeichnis erstellen
    result = requests.post(requestUrl + getFolders, headers = headers,
                           auth = HttpNtlmAuth(username, password))

    #  Request Status Code überprüfen
    if isBadRequest(result.status_code):
        print("Anfrage fehlgeschlagen. Status Code:", result.status_code)
        print("Verzeichnisse konnte nicht erstellt werden.")
        return False
    else:
        print("Verzeichnis '" + newDirName + "' erfolgreich erstellt.")
        return True


def printFiles(username, password, requestUrl, serverRelativeUrl, digestValue):
    """ Listet alle Dateien in einem SharePoint Verzeichnis auf.

        :param username: Der Benutzername.
        :param password: Das Benutzer Passwort.
        :param requestUrl: Die URL zur SharePoint Webseite bzw. Unterwebseite.
        :param serverRelativeUrl: Relativer Serverpfad welcher das Upload
                                  Verzeichnis spezifiziert.
        :param digestValue: Der Digest Value authentifiziert den Benutzer.
    """
    #  Header zum auflisten der Dateien vorbereiten.
    headers = {'Content-Type': 'application/json; odata=verbose',
               'accept': 'application/json;odata=verbose',
               'x-requestdigest': digestValue}

    # Relativer Pfad zum SharePoint Verzeichnis
    getFiles = "_api/web/GetFolderByServerRelativeUrl('" + serverRelativeUrl \
        + "')/files"

    #  Dateien ausgeben
    result = requests.post(requestUrl + getFiles, headers = headers,
                           auth = HttpNtlmAuth(username, password))

    #  Request Status Code überprüfen
    if isBadRequest(result.status_code):
        print("Anfrage fehlgeschlagen.")
        print("Dateien können nicht ausgeben werden.")
        return

    # Digest Value aus der JSON auslesen
    if isJSON(result.content):
        files = result.json()['d']['results']
        for file in files:
            print(file['Name'])
    else:
        print("Keine valide JSON-Datei!")
        print("Dateien können nicht ausgeben werden.")
