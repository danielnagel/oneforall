from distutils.dir_util import copy_tree


def synchronise(src, dst):
    """ Kopiert alle Dateien eines Verzeichnisses in ein anderes.
        Dateien welche im Zielverzeichnis nicht benötigt werden, werden
        entfernt.
    """
    copy_tree(src, dst)
