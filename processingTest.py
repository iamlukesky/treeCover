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

app = QgsApplication(sys.argv, True)
QgsApplication.initQgis();
QgsApplication.setPrefixPath('/usr', True)
Processing.initialize()

# Processing directory
cwd = os.getcwd()
procdir = cwd + '/LST-trad/hojd/'
outdir = cwd + '/LST-trad/treecover2/'
filterfile = cwd + "/LST-trad/qgis5x5filter_1or0_div1.txt"
files = os.listdir(procdir)
#files = [f for f in os.listdir(procdir) if os.path.isfile(f)]
# Filter files
#filefilt =[]
#for f in files:
    #if f.endswith(".tif"):
        #filefilt.append(f)

print "startar"

#print "help:"
#alghelp("saga:rastercalculator")
#alghelp("grass:r.mfilter")

inputraster = procdir + "/THL_66_6_0025.tif"
outputraster = outdir + "/uttest.tif"

fileInfo = QFileInfo(inputraster)
baseName = fileInfo.baseName()
rlayer = getObject(inputraster)

extent = rlayer.extent()
xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

print "rascal 1"
outputs_SAGARASTERCALCULATOR_1=runalg('saga:rastercalculator', inputraster,[],'ifelse(a > 50, 1, 0)',True,1,None)

print "mfilter"
outputs_GRASS7R_MFILTER_1=runalg('grass7:r.mfilter', outputs_SAGARASTERCALCULATOR_1['RESULT'],filterfile,1.0,False,"%f,%f,%f,%f"% (xmin, xmax, ymin, ymax),0.0,None)

print "rascal 2"
outputs_SAGARASTERCALCULATOR_2=runalg('saga:rastercalculator', outputs_GRASS7R_MFILTER_1['output'],[],'a * 4',True,1,outputraster)

print "done"

#QgsApplication.exitQgis();
