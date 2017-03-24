from qgis.core import *
from qgis.gui import *
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt


app = QgsApplication(sys.argv, True)
QgsApplication.initQgis();
QgsApplication.setPrefixPath('/usr', True)

sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
from processing.tools import *

Processing.initialize()
print Processing.getAlgorithm("qgis:creategrid")


# Processing directory
cwd = os.getcwd()
procdir = cwd + '/LST-trad/hojd/'
tmpdir = cwd + '/LST-trad/Test2/'
outdir = cwd + '/LST-trad/treecover2/'
#procdir = "D:/Projekt/2017/LST-trad/hojd/"
#tmpdir = "D:/Projekt/2017/LST-trad/Test2/"
#outdir = "D:/Projekt/2017/LST-trad/treecover2/"
filter = "qgis5x5filter_1or0_div1.txt"
files = os.listdir(procdir)
#files = [f for f in os.listdir(procdir) if os.path.isfile(f)]
# Filter files
filefilt =[]
for f in files:
    if f.endswith(".tif"):
        filefilt.append(f)
        
print "hej"
# List with files

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
    
#print arglist

formula1 =('ifelse(a > 50, 1, 0)')
formula2 = ('a * 4')



for arg in arglist:
    tmp1 = tmpdir + "t1_" + arg[3]
    tmp2 = tmpdir + "t2_" + arg[3]
    print "saga"
    Processing.runAlgorithm("saga:rastercalculator", arg[0], None, formula1, True, 1, tmp1)
    print "grass"
    Processing.runAlgorithm("grass:r.mfilter", tmp1, filter,1,False,arg[1],0, tmp2)
    print "rascal"
    Processing.runAlgorithm("saga:rastercalculator", tmp2, None, formula2, True, 1, arg[2])
    

#QgsApplication.exitQgis();

