import sys


class NullWriter(object):
    """ Diese Klasse ueberschreibt die Funktion write(), damit alle
        Schreibvorgaenge ignoriert werden.
    """
    def write(self, arg):
        pass


def mute_stdout(callback, *args):
    """ Deaktiviert Ausgaben nach stdout fuer eine Funktion und Aktiviert
        stdout anschliessend wieder.
        Gibt die Rueckgabe der callback-Funktion zurueck.
    """
    nullwrite = NullWriter()
    oldstdout = sys.stdout
    sys.stdout = nullwrite  # stdout deaktivieren
    result = callback(*args)
    sys.stdout = oldstdout  # stdout aktivieren
    return result


def mute_stderr(callback, *args):
    """ Deaktiviert Ausgaben nach stderr fuer eine Funktion und Aktiviert
        stderr anschliessend wieder.
        Gibt die Rueckgabe der callback-Funktion zurueck.
    """
    nullwrite = NullWriter()
    oldstderr = sys.stderr
    sys.stderr = nullwrite   # stderr deaktivieren
    result = callback(*args)
    sys.stderr = oldstderr   # stderr aktivieren
    return result
