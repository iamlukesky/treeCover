Hämta skripten
==============

Skripten kan laddas ner som zip
[här](https://github.com/iamlukesky/treeCover/archive/master.zip). Eller
klona med git: `https://github.com/iamlukesky/treeCover.git`.

Installation / beroenden
========================

Windows
-------

Installera QGIS, GRASS och SAGA med OSGEO4W installern (advanced
install) och välj följande versioner:

-   <span>**QGIS:**</span> Skripten testade med 2.18.4, men för just
    QGIS verkar exakt version mindre viktig.

-   <span>**SAGA:**</span> 2.1.2-2 (ej saga-ltr)

-   <span>**GRASS:**</span> 7.2.0-1

### Ubuntu

Installera Qgis via `apt-get`, SAGA och GRASS enligt instruktioner i
[det här gis.stackxchange
svaret](http://gis.stackexchange.com/a/225520/62427).

Användning
==========

`treeCover.py` förväntar sig att köras i en mapp med mapparna `Input`,
där de filer som ska processas ska ligga, och `Output` för
färdigprocessade filer.

Windows
-------

Kör `win.bat`, den sätter nödvändiga miljövariabler och startar
pythonscriptet. Eventuellt kan filen behöva redigeras för att ange rätt
OSGEO4W-mapp om du har valt något annat än standard.

Ubuntu
------

Alla python bindings görs när Qgis installeras via apt-get. Scriptet ska
gå att köra rakt av med `python treeCover.py`.

Skriva nya script
=================

Skriptet `pyQgis-headless-blank.py` är tänkt att fungera som en
boilerplate för att göra nya script. Utöver de obligatoriska
bibliotekimporterna finns även lite hjälpfunktioner, som att sätta
extent programmatiskt på ett sätt som GRASS tycker om och en funktion
för att sortera ut alla filer med en viss filändelse.

Ett arbetsflöde som fungerar smidigt är att experimentera med
Processing-toolboxen i qgis för att se att verktyget gör det man vill.
Sen gå till `Processing -> History` och plocka python-snippeten för
verktyget, `processing.runalg(…)` och stoppa in det i sitt script. För
att få veta vilka argument varje funktion tar, kör
`processing.alghelp(algoritmen)`.
