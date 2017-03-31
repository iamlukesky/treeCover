from qgis.core import *
from qgis.gui import *
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt

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
tmpdir = cwd + '/LST-trad/Test2/'
outdir = cwd + '/LST-trad/treecover2/'
filter = cwd + "/LST-trad/qgis5x5filter_1or0_div1.txt"
files = os.listdir(procdir)
#files = [f for f in os.listdir(procdir) if os.path.isfile(f)]
# Filter files
filefilt =[]
for f in files:
    if f.endswith(".tif"):
        filefilt.append(f)

print "startar"

#print "help:"
#alghelp("saga:rastercalculator")
#alghelp("grass:r.mfilter")

# Coordinates
arglist = []
for file in filefilt:
    x1 = int(file[7] + file[11:13]+"000")
    x2 = x1 + 25000
    y1 = int(file[4:6] + file[9:11] +"000")
    y2 = y1 + 25000
    coords =  str(x1) + "," + str(x2) + "," + str( y1) + "," + str(y2)
    outfile = "COV_" + file[4:]
    arglist.append([procdir+file, coords, outdir+outfile, outfile])

formula1 =('ifelse(a > 50, 1, 0)')
formula2 = ('a * 4')

for arg in arglist:
    tmp1 = tmpdir + "t1_" + arg[3]
    tmp2 = tmpdir + "t2_" + arg[3]
    print "saga"
    #first_op = getObject(arg[0])
    first_op = arg[0]
    runalg("saga:rastercalculator", first_op, None, formula1, True, 1, tmp1)
    print "grass"
    second_op = getObject(tmp1)
    #runalg("grass:r.mfilter", second_op, filter,1,False,"625000.0,650000.0,6600000.0,6625000.0", 0, tmp2)
    runalg("grass7:r.mfilter","/home/johnnie/GiB/Projekt/qgisHeadless/LST-trad/Test2/t1_COV_66_6_0025.tif","/home/johnnie/GiB/Projekt/qgisHeadless/LST-trad/qgis5x5filter_1or0_div1.txt",1,False,"625000.0,650000.0,6600000.0,6625000.0",0,None)
    print "rascal"
    print "object"
    #third_op = getObject(result)
    third_op = tmp2
    print "alg"
    runalg("saga:rastercalculator", third_op, None, formula2, True, 1, arg[2])

QgsApplication.exitQgis();
