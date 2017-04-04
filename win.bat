SET OSGEO4W_ROOT=C:\OSGeo4W64

SET QGIS_PREFIX=%OSGEO4W_ROOT%\apps\qgis

SET PATH=%QGIS_PREFIX%\bin;%OSGEO4W_ROOT%\bin;%QGIS_PREFIX%\python\plugins;%PATH%

SET PYTHONPATH=%QGIS_PREFIX%\python;%OSGEO4W_ROOT%\apps\Python27;%QGIS_PREFIX%\python\plugins\processing;%PYTHONPATH%

SET PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27

SET GDAL_DATA=%OSGEO4W_ROOT%\share\gdal

python treeCover.py