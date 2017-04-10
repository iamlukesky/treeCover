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
import gdal_merge

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

print "startar"
# Set input/output directories
# cwd = the directory where the script gets called.
cwd = os.getcwd()
procdir = os.path.join(cwd, 'LST-trad', 'hojd')
outdir = os.path.join(cwd, 'LST-trad','treecover2')
# filter definition for grass:r.mfilter
filterfile = os.path.join(cwd, 'LST-trad', 'qgis5x5filter_1or0_div1.txt')

# filter to get all of the .tif files in the input directory
inputfiles = []
for file in os.listdir(procdir):
    if file.endswith(".tif"):
        inputfiles.append(os.path.join(procdir, file))

# expressions used in the Saga raster calculator
saga_expression_1 = 'ifelse(a > 50, 1, 0)'
saga_expression_2 = 'a * 4'

# for merging the results
outputfiles = []

for file in inputfiles:
    basename = QFileInfo(file).baseName()
    print "starting: ", basename
    inputraster = file
    outputraster = "COV_" + basename + ".tif"
    outputraster = os.path.join(outdir, outputraster)
    extent = getExtent(inputraster)

    print "rascal 1"
    outputs_SAGARASTERCALCULATOR_1=processing.runalg('saga:rastercalculator',
                                          inputraster,[],saga_expression_1,True,1,None)

    print "mfilter"
    outputs_GRASS7R_MFILTER_1=processing.runalg('grass7:r.mfilter',
                                 outputs_SAGARASTERCALCULATOR_1['RESULT'],filterfile,1.0,False,extent,0.0,None)

    print "rascal 2"
    outputs_SAGARASTERCALCULATOR_2=processing.runalg('saga:rastercalculator',
                                          outputs_GRASS7R_MFILTER_1['output'],[],saga_expression_2,True,1,outputraster)

    print "done with: ", basename, ", output as :", outputraster

    if len(inputfiles) > 1:
        outputfiles.append(outputraster)


print "done, no more inputfiles"
#if len(outputfiles) > 0:
    #print "merging outputs"
    #tomerge = ";".join(outputfiles)
    #mergeOutput = os.path.join(outdir, "merge.tif")
    #sys.argv = ['-ot', 'Byte', '-o', mergeOutput] + outputfiles
    #print tomerge
    #outputs_GDAL_MERGE = processing.runalg("gdalogr:merge", tomerge, False,
                                           #False, 0, mergeOutput)
    #gdal_merge.main()
    #print "done merging"
#QgsApplication.exitQgis();

#processing.runalg("gdalogr:merge","/home/johnnie/GiB/Projekt/qgisHeadless/LST-trad/mergetest/subset;/home/johnnie/GiB/Projekt/qgisHeadless/LST-trad/treecover2/COV_THL_66_6_0025.tif",False,False,1,None)
