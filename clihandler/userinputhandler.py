def checkSlash(string, start=True):
    """ Prüft ob ein Schrägstrich am Anfang oder am Ende eines Strings
        vorhanden ist.

        :param string: Der zu überprüfende String.
        :param index: Wenn True wird geprüft ob ein Slash am Anfang ist, bei
                      False wird der Ende des Strings überprüft.
        :return: True wenn ein Slash an der richtigen Stelle gefunden wurde,
                 ansonsten False.
    """
    if(start):
        if(string.find('/') is not -1):
            return True
        else:
            return False
    else:
        if(string.find('/', len(string) - 2) is not -1):
            return True
        else:
            return False


def addMissingSlash(string, start=True, end=True):
    """ Fügt keinen, einen oder zwei Schrägstriche an einen String an.

        :param string: Der zu manipulierende String.
        :param start: Bei True wird ein Schrägstrich an den Anfang des Strings
                      gehängt, bei False nicht.
        :param end: Bei True wird ein Schrägstrich an das Ende des Strings
                      gehängt, bei False nicht.
        :return: Der angepasste String.
    """
    if(start):
        if(checkSlash(string) is False):
            string = "/" + string
    if(end):
        if(checkSlash(string, False) is False):
            string = string + "/"
    return string
