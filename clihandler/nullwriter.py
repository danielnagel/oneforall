import sys


class NullWriter(object):
    """ Diese Klasse überschreibt die Funktion write(), damit alle
        Schreibvorgänge ignoriert werden.
    """
    def write(self, arg):
        pass


def mute_stdout(callback, *args):
    """ Deaktiviert Ausgaben nach stdout für eine Funktion und Aktiviert
        stdout anschließend wieder.
        Gibt die Rückgabe der callback-Funktion zurück.
    """
    nullwrite = NullWriter()
    oldstdout = sys.stdout
    sys.stdout = nullwrite  # stdout deaktivieren
    result = callback(*args)
    sys.stdout = oldstdout  # stdout aktivieren
    return result


def mute_stderr(callback, *args):
    """ Deaktiviert Ausgaben nach stderr für eine Funktion und Aktiviert
        stderr anschließend wieder.
        Gibt die Rückgabe der callback-Funktion zurück.
    """
    nullwrite = NullWriter()
    oldstderr = sys.stderr
    sys.stderr = nullwrite   # stderr deaktivieren
    result = callback(*args)
    sys.stderr = oldstderr   # stderr aktivieren
    return result
