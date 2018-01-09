from os import listdir, remove
from os.path import isfile, join, exists
from clihandler.nullwriter import mute_stderr
from slimit import minify


def isextension(extension, file):
    """ True wenn ein String mit einem bestimmten Suffix endet.
    """
    return file.endswith(extension)


def remove_oldfile(dirpath, oldfile):
    """ Wenn eine zusammengefasste Datei bereits vorhanden ist soll diese
        entfernt werden, da die bestehende Datei sonst erweitert werden würde.
    """
    if exists(join(dirpath, oldfile)):
        print("Entferne alte Datei:", oldfile)
        remove(join(dirpath, oldfile))


def list_files(dirpath, extension):
    """ Schreibt den Namen aller Dateien innerhalb eines Verzeichnisses in eine
        Liste und gibt diese zurück.
        Wurde keine Datei gefunden, wird eine leere Liste zurückgegeben.
    """
    onlyfiles = [file for file in listdir(dirpath)
                if isfile(join(dirpath, file)) and isextension(extension, file)]
    if len(onlyfiles) < 1: # Keine Dateien gefunden.
        print("Keine Dateien mit der Endung '" + extension + "' gefunden.")
    return onlyfiles


def join_files(filelist, dirpath, minifyjs):
    """ Liest den Inhalt der Dateien in der Liste und fügt deren Inhalt zu
        einem String zusammen und gibt diesen zurück.
        Ist die Option minifyjs=True wird die Datei komprimiert.
    """
    filecontentin = ""
    for file in filelist:
        filestreamin = open(join(dirpath, file), "r")
        filecontentin += filestreamin.read();
        filestreamin.close()

    if(minifyjs):
        filecontentin = mute_stderr(minify, filecontentin, True)

    return filecontentin


def write_newfile(dirpath, outfile, newfilecontent):
    """ Schreibt den zusammengefassten (und evtl. komprimierten) Dateieninhalt
        in eine Datei.
    """
    filestreamout = open(join(dirpath, outfile), "a")
    filestreamout.write(newfilecontent + "\n")
    filestreamout.close()
    print("Neu erstellte Datei: ", outfile)


def merge_files(dirpath, outfile, extension, minifyjs):
    """ Fügt mehrere Dateien, innerhalb eines Verzeichnisses, zu einer zusammen
        und kompremiert JavaScript-Dateien, wenn dies gewünscht ist.
    """
    print("\nFühre Dateien im Verzeichnis '" + dirpath + "' zusammen.")
    if(minifyjs):
        outfile += ".min." + extension
    else:
        outfile += "." + extension
    remove_oldfile(dirpath, outfile)
    filelist = list_files(dirpath, extension)
    if(len(filelist) < 1):
        print("Zusammenführung abgebrochen.")
        return
    newfilecontent = join_files(filelist, dirpath, minifyjs)
    write_newfile(dirpath, outfile, newfilecontent)
    print("Zusammenführung abgeschlossen.")
