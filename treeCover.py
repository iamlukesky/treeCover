print "importing"
from qgis.core import *
from qgis.gui import *
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QFileInfo

sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
#import processing.tools.general as processing
from processing.tools.dataobjects import *
from processing.tools.general import *
from processing.tools.vector import *
from processing.tools.raster import *
from processing.tools.system import *

print "initializing"
app = QgsApplication(sys.argv, True)
QgsApplication.setPrefixPath('/usr', True)
QgsApplication.initQgis();

Processing.initialize()

def getExtent(extentRaster):
    fileInfo = QFileInfo(inputraster)
    baseName = fileInfo.baseName()
    rlayer = getObject(inputraster)

    extent = rlayer.extent()
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()
    return "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax)

print "startar"

#print "help:"
#alghelp("saga:rastercalculator")
#alghelp("grass:r.mfilter")

# Processing directory
cwd = os.getcwd()
procdir = cwd + '/LST-trad/hojd/'
outdir = cwd + '/LST-trad/treecover2/'
filterfile = cwd + "/LST-trad/qgis5x5filter_1or0_div1.txt"

inputfiles = []
for file in os.listdir(procdir):
    if file.endswith(".tif"):
        inputfiles.append(os.path.join(procdir, file))

saga_expression_1 = 'ifelse(a > 50, 1, 0)'
saga_expression_2 = 'a * 4'

for file in inputfiles:
    basename = QFileInfo(file).baseName()
    print "starting: ", basename
    inputraster = file
    outputraster = "COV_" + basename + ".tif"
    outputraster = outdir + outputraster
    # extent is used for Grass commands since they are picky
    # with how the extent is defined. Other commands can usually use None as
    # extent to use the entire file.
    extent = getExtent(inputraster)

    print "rascal 1"
    outputs_SAGARASTERCALCULATOR_1=runalg('saga:rastercalculator',
                                          inputraster,[],saga_expression_1,True,1,None)

    print "mfilter"
    outputs_GRASS7R_MFILTER_1=runalg('grass7:r.mfilter',
                                 outputs_SAGARASTERCALCULATOR_1['RESULT'],filterfile,1.0,False,extent,0.0,None)

    print "rascal 2"
    outputs_SAGARASTERCALCULATOR_2=runalg('saga:rastercalculator',
                                          outputs_GRASS7R_MFILTER_1['output'],[],saga_expression_2,True,1,outputraster)

    print "done with: ", basename
    print "output: ", outputraster

print "done, no more inputfiles"
#QgsApplication.exitQgis();

