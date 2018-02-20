import sys
from filehandler.filehandler import copyFiles, removeFiles, list_files
from filehandler.minify import merge_files
from sharepointhandler.sharepointhandler import getDigestValue, uploadFile, createFolder
from clihandler.userinputhandler import addMissingSlash
from optparse import OptionParser
from getpass import getpass

usage = "Nutzung: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-s", "--sourcedir", action="store", type="string",
                  dest="srcpath", default=".",
                  help="JS Verzeichnis oder Projektverzeichnis.")
parser.add_option("-o", "--outfile", action="store", type="string",
                  dest="outfile", default="oneforall",
                  help="Ausgabedatei der zusammengefassten JS.")
parser.add_option("-u", "--subsite", action="store", type="string",
                  dest="subsite", default=".",
                  help="Unterwebseite des SharePoint Projekts.")
parser.add_option("-r", "--relative-url", action="store", type="string",
                  dest="relative", default=".",
                  help="Relativer Pfad zu den Projektdateien (SharePoint).")
(options, args) = parser.parse_args(sys.argv)

#  Quell Verzeichnis in ein temporäres Arbeitsverzeichnis kopieren.
copyFiles(options.srcpath, "./temp")
#  Alle JavaScript Dateien zu einer Minified Datei zusammenfassen.
merge_files("./temp/js", options.outfile)
#  Alle JavaScript Dateien außer der Minified Datei entfernen.
removeFiles("./temp/js")

if(options.subsite is "."):
    print("Projekt wird nicht ins SharePoint kopiert.")
else:
    #  SharePoint URL und Ziel Bibliothek.
    sharePointUrl = 'https://sharepoint.propersonal.de'
    subSiteUrl = addMissingSlash(options.subsite)
    #  Request URL vorbereiten.
    requestUrl = sharePointUrl + subSiteUrl
    serverRelativeUrl = addMissingSlash(options.relative, False)
    # Benutzerdaten abfragen.
    username = input("Benutzernamen eingeben: ")
    password = getpass("Passwort eingeben: ")
    # Dateien des Wurzelverzeichnisses hochladen.
    files = list_files("./temp")
    digestValue = getDigestValue(username, password, requestUrl)
    for file in files:
        uploadFile(username, password, "./temp", file, requestUrl,
                   serverRelativeUrl, digestValue)
    # Dateien des CSS Verzeichnisses hochladen.
    files = list_files("./temp/css")
    if(createFolder(username, password, requestUrl, serverRelativeUrl, 'css',
       digestValue)):
        for file in files:
            uploadFile(username, password, "./temp/css", file, requestUrl,
                       serverRelativeUrl + "/css", digestValue)
    # Dateien des JS Verzeichnisses hochladen.
    files = list_files("./temp/js")
    if(createFolder(username, password, requestUrl, serverRelativeUrl, 'js',
       digestValue)):
        for file in files:
            uploadFile(username, password, "./temp/js", file, requestUrl,
                       serverRelativeUrl + "/js", digestValue)
