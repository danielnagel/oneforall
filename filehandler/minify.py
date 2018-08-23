from clihandler.nullwriter import mute_stderr
from filehandler import remove_oldfile, list_files_byextension
from slimit import minify
from os.path import join


def join_files(filelist, dirpath):
    """ Liest den Inhalt der Dateien in der Liste und fuegt deren Inhalt zu
        einem String zusammen und gibt diesen zurueck.
        Ist die Option minifyjs=True wird die Datei komprimiert.
    """
    filecontentin = ""
    for file in filelist:
        filestreamin = open(join(dirpath, file), "r")
        filecontentin += filestreamin.read()
        filestreamin.close()

    #  Zusammengefuehrte Dateien verkleinern.
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


def merge_files(dirpath, outfile):
    """ Fuegt mehrere Dateien, innerhalb eines Verzeichnisses, zu einer zusammen
        und kompremiert JavaScript-Dateien, wenn dies gewuenscht ist.
    """
    extension = "js"
    print("\nFuehre Dateien im Verzeichnis '" + dirpath + "' zusammen.")
    outfile += ".min." + extension
    remove_oldfile(dirpath, outfile)
    filelist = list_files_byextension(dirpath, extension)
    if(len(filelist) < 1):
        print("Zusammenfuehrung abgebrochen.")
        return
    newfilecontent = join_files(filelist, dirpath)
    write_newfile(dirpath, outfile, newfilecontent)
    print("Zusammenfuehrung abgeschlossen.")
