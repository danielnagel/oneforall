# OneForAll #

OneForAll ist ein Tool mit dem alle Schritte bei der Entwicklung einer SharePoint Webapp anfallen automatisiert werden.

> ## ACHTUNG ##
>
> Das Tool befindet sich noch in der Entwicklung und ist daher noch nicht ausgiebig auf Fehler getestet worden.

### Wie verwende ich OneForAll? ###

In der Eingabeaufforderung:
 * python oneforall.py \[option\]

Optionen:
 * -h, --help
   * Zeigt alle Optionen an.
 * -s SRCPATH, --sourcedir=SRCPATH
   * JS Verzeichnis oder Projektverzeichnis
 * -o OUTFILE, --output=OUTFILE
   * Ausgabedatei der zusammengefassten JS
 * -m, --minify
   * JS komprimieren
 * -e EXTENSION, --extension=EXTENSION
   * Nach bestimmter Dateiendung Daten zusammenfassen
 * -d DSTPATH, --destdir=DSTPATH
   * Zielverzeichnis für eine Kopie des Projekts
 * -p, --sharepoint
   * Aktiviert Passwortabfrage und SharePoint Verzeichnisse

### Wer ist verantwortlich für dieses Projekt? ###

 * Daniel