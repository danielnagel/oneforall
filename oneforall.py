import sys
from filehandler.minify import merge_files
from synchronisehandler.synchroniser import synchronise
from optparse import OptionParser

usage = "Nutzung: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-s", "--sourcedir", action="store", type="string",
                  dest="srcpath", default=".",
                  help="JS Verzeichnis oder Projektverzeichnis")
parser.add_option("-o", "--output", action="store", type="string",
                  dest="outfile", default="allforone",
                  help="Ausgabedatei der zusammengefassten JS")
parser.add_option("-m", "--minify", action="store_true", dest="minifyjs",
                  default=False, help="JS komprimieren")
parser.add_option("-e", "--extension", action="store", type="string",
                  dest="extension", default="js",
                  help="Nach bestimmter Dateiendung Daten zusammenfassen")
parser.add_option("-d", "--destdir", action="store", type="string",
                  dest="dstpath", default=".",
                  help="Zielverzeichnis für eine Kopie des Projekts")
parser.add_option("-p", "--sharepoint", action="store_true", dest="sharepoint",
                  default=False,
                  help="Aktiviert Passwortabfrage und SharePoint Verzeichnisse")
(options, args) = parser.parse_args(sys.argv)

if "." in options.extension:
    print("Bitte nur die Dateiendung ohne '.' eingeben.")
    sys.exit(0)

merge_files(options.srcpath, options.outfile, options.extension, options.minifyjs)

synchronise(options.srcpath, options.dstpath)
