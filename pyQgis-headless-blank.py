print "importing"
from qgis.core import *
import os, sys
from PyQt4.QtCore import Qt, QFileInfo

#Needed to make python aware of where Processing is
if sys.platform.startswith('linux'):
    sys.path.append('/usr/share/qgis/python/plugins')
    sys.path.append('/usr/bin/') # for gdal_merge
elif sys.platform.startswith('win'):
    sys.path.append('C:\\OSGeo4W64\\apps\\qgis\\python\\plugins')

import processing
from processing.core.Processing import Processing

print "initializing"
app = QgsApplication(sys.argv, True)
if sys.platform.startswith('linux'):
    QgsApplication.setPrefixPath('/usr', True)
elif sys.platform.startswith('win'):
    QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis', True)

QgsApplication.initQgis();
Processing.initialize()
Processing.updateAlgsList()

# getExtent is used for Grass commands since they are picky
# with how the extent is defined. Other commands can usually use None as
# extent to use the entire file.
def getExtent(extentRaster):
    fileInfo = QFileInfo(extentRaster)
    baseName = fileInfo.baseName()
    rlayer = processing.getObject(extentRaster)

    extent = rlayer.extent()
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()
    return "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax)

def filterFiles(extension):
    filteredFiles = []
    for file in os.listdir(procdir):
        if file.endswith(extension):
            filteredFiles.append(os.path.join(procdir, file))
    return filteredFiles


# Set input/output directories
cwd = os.getcwd()
procdir = os.path.join(cwd, 'Input')
outdir = os.path.join(cwd, 'Output')

# filter to get all of the files in input directry with desired extension
inputfiles = filterFiles(".tif")

for file in inputfiles:
    basename = QFileInfo(file).baseName()
    print "starting: ", basename
    inputraster = file
    outputraster = "out_" + basename + ".tif"
    outputraster = os.path.join(outdir, outputraster)
    extent = getExtent(inputraster)


    #processing toolbox function calls here


    print "done with: ", basename, ", output as :", outputraster

    if len(inputfiles) > 1:
        outputfiles.append(outputraster)


print "done, no more inputfiles"
