import sys
from filehandler.minify import merge_files

# Bei zu wenig Kommadozeilen Argumenten wird das Programm beendet.
if len(sys.argv) < 4:
    print("Zu weninge Argumente!")
    print("Nutzung:")
    print(sys.argv[0], " <Dateiendung> <Verzeichnis> <Ausgabedateiname> [minify]")
    sys.exit(0)

extension = sys.argv[1]
dirpath = sys.argv[2]
outfile = sys.argv[3]
minifyjs = False
if(len(sys.argv) == 5):
    minifyjs = True

if "." in extension:
    print("Bitte nur die Dateiendung ohne '.' eingeben.")
    sys.exit(0)

merge_files(dirpath, outfile, extension, minifyjs)
