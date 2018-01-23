from shutil import copytree, rmtree, ignore_patterns
from os import listdir, remove, walk, chmod
from os.path import isfile, join, exists, isdir
from filehandler.filehandler import isextension
import stat

def synchronise(src, dst):
    """ Kopiert alle Dateien eines Verzeichnisses in ein anderes.
        Dateien welche im Zielverzeichnis nicht benötigt werden, werden
        entfernt.
    """
    if isdir("./temp"):
        rmtree("./temp", onerror=remove_readonly)
    copytree(src, "./temp", ignore=ignore_patterns('.git*', '*.md', 'doc'))
#    changeMod("./temp")

def removeFiles(path):
    for file in listdir(path):
        if isfile(join(path, file)) and isextension('js', file):
            if not isextension('min.js', file):
                remove(join(path, file))

def remove_readonly(func, path, _):
    "Setze das Schreiben Bit und entferne die Datei."
    os.chmod(path, stat.S_IWRITE)
    func(path)
