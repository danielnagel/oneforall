from clihandler.nullwriter import mute_stderr
from filehandler.filehandler import remove_oldfile, list_files
from slimit import minify
from os.path import join



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
