# OneForAll #

OneForAll ist ein Tool mit dem alle Schritte bei der Entwicklung einer
SharePoint Webapp anfallen automatisiert werden.

1. Zusammenfassen und kompremieren aller JavaScript Dateien.
2. Hochladen aller Dateien ins SharePoint.

Diese Schritte können auch getrennt voneinander ausgeführt werden.

> ## ACHTUNG ##
>
> Das Tool befindet sich noch in der Entwicklung und ist daher noch nicht ausgiebig auf Fehler getestet worden.

### Wie verwende ich OneForAll? ###

In der Eingabeaufforderung

* python oneforall.py \[option\]

Optionen

* -h, --help
    * Zeigt alle verfügbaren Optionen an.
* -s SRCPATH, --sourcedir=SRCPATH
    * JS Verzeichnis oder Projektverzeichnis
* -o OUTFILE, --outfile=OUTFILE
    * Ausgabedatei der zusammengefassten JS
* -u SUBSITE, --subsite=SUBSITE
    * Unterwebseite des SharePoint Projekts.
* -r RELATIVE, --relative-url=RELATIVE
    * Relativer Pfad zu den Projektdateien (im SharePoint).

### Geplante Erweiterung für OneForAll ###

* Dynamisches erstellen der benötigten Projektstruktur.

### Wer ist verantwortlich für dieses Projekt? ###

* Daniel
