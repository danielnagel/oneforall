from os import listdir, remove, chmod
from os.path import isfile, join, exists, isdir
from shutil import copytree, rmtree, ignore_patterns


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


def list_files_byextension(dirpath, extension):
    """ Schreibt den Namen aller Dateien, mit bestimmter Endung, innerhalb
        eines Verzeichnisses in eine Liste und gibt diese zurück.
        Wurde keine Datei gefunden, wird eine leere Liste zurückgegeben.
    """
    onlyfiles = [file for file in listdir(dirpath)
                 if isfile(join(dirpath, file))
                 and isextension(extension, file)]
    if len(onlyfiles) < 1:
        #  Keine Dateien gefunden.
        print("Keine Dateien mit der Endung '" + extension + "' gefunden.")
    return onlyfiles


def list_files(dirpath):
    """ Schreibt den Namen aller Dateien innerhalb eines Verzeichnisses in eine
        Liste und gibt diese zurück.
        Wurde keine Datei gefunden, wird eine leere Liste zurückgegeben.
    """
    onlyfiles = [file for file in listdir(dirpath)
                 if isfile(join(dirpath, file))]
    return onlyfiles


def copyFiles(src, dst):
    """ Kopiert alle Dateien eines Verzeichnisses in ein anderes.
        Dateien welche im Zielverzeichnis nicht benötigt werden, werden
        entfernt.
    """
    if isdir(dst):
        rmtree(dst, onerror=remove_readonly)
    copytree(src, dst, ignore=ignore_patterns('.git*', '*.md', 'doc',
                                                   'res*', 'Test*', 'ver*'))


def removeFiles(path):
    """ Löscht alle JavaScript Dateien die nicht die Endung 'min.js' haben.
    """
    for file in listdir(path):
        if isfile(join(path, file)) and isextension('js', file):
            if not isextension('min.js', file):
                remove(join(path, file))


def remove_readonly(func, path, _):
    """ Setze das Schreiben Bit und entferne die Datei.
    """
    chmod(path, stat.S_IWRITE)
    func(path)
