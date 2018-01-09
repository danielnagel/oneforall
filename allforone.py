from os import listdir, remove
from os.path import isfile, join, exists
import sys
from clihandler.nullwriter import mute_stderr
#from optparse import OptionParser
# Slimit Packet muss installiert werden: pip install slimit
from slimit import minify


def isextension(extension, file):
    "True wenn ein String mit einem bestimmten Suffix endet."
    return file.endswith(extension)



# minify = False

#parser = OptionParser()
#parser.add_option("-m", "--minify", action="store_true", dest="verbose", default=False)

# Bei zu wenig Kommadozeilen Argumenten wird das Programm beendet.
if len(sys.argv) < 4:
    print("Zu weninge Argumente!")
    print("Nutzung:")
    print(sys.argv[0], " <Dateiendung> <Verzeichnis> <Ausgabedateiname> [minify]")
    sys.exit(0)

extension = sys.argv[1]
dirpath = sys.argv[2]
fileout = sys.argv[3]

if "." in extension:
    print("Bitte nur die Dateiendung ohne '.' eingeben.")
    sys.exit(0)

if(len(sys.argv) == 5):
    fileout += ".min." + extension
else:
    fileout += "." + extension

# Wenn eine zusammengefasste Datei bereits vorhanden ist soll diese entfernt
# werden, da die bestehende Datei sonst erweitert werden würde.
if exists(join(dirpath, fileout)):
    remove(join(dirpath, fileout))

# durch 'list comprehension' wird das Ergebnis jedes Schleifendurchlaufs in
# file gespeichert.
onlyfiles = [file for file in listdir(dirpath) if isfile(join(dirpath, file)) and isextension(extension, file)]

# Wurden keine dateien gefunden wird das Programm beendet.
if len(onlyfiles) < 1:
    print("Keine Dateien mit der Endung '" + extension + "' gefunden.")
    sys.exit(0)

# Lesen der Dateien in der Liste und schreiben des Inhalts in eine Datei.
#filestreamout = open(join(dirpath, fileout), "a")
filecontentin = ""

for file in onlyfiles:
    filestreamin = open(join(dirpath, file), "r")
    #filestreamout.write(filestreamin.read() + "\n")
    filecontentin += filestreamin.read();
    filestreamin.close()

if(len(sys.argv) == 5):
    filecontentin = mute_stderr(minify, filecontentin, True)

filestreamout = open(join(dirpath, fileout), "a")
filestreamout.write(filecontentin + "\n")
filestreamout.close()

print("Dateien zusammengefasst.")
print("Neu erstellte Datei: ", fileout)
