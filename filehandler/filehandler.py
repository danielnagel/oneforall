from os import listdir, remove
from os.path import isfile, join, exists


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
    if len(onlyfiles) < 1: #  Keine Dateien gefunden.
        print("Keine Dateien mit der Endung '" + extension + "' gefunden.")
    return onlyfiles
