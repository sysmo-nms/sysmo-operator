#!/usr/bin/env python

from    PySide.QtGui    import QApplication
from    PySide.QtCore   import QSettings
import  sys
import  re
import  platform
import  noctopus_main


osType           = platform.platform()
noctopusSettings = QSettings("Noctopus NMS", "noctopus-client")
noctopusStyle    = noctopusSettings.value("NMainWindow/style")

if noctopusStyle == None:
    if   re.match('^Windows-XP..*',    osType) != None:
        noctopusStyle = 'plastique'
    elif re.match('^Linux..*',         osType) != None:
        noctopusStyle = 'plastique'
    elif re.match('^Windows-Vista..*', osType) != None: pass # native
    elif re.match('^Windows-7..*',     osType) != None: pass # native
    elif re.match('^Windows-8..*',     osType) != None: pass # native
    elif re.match('^Mac..*',           osType) != None: pass # native

if noctopusStyle != None:
    QApplication.setStyle(noctopusStyle)

noctopusApp  = QApplication(sys.argv)
currentStyle = noctopusApp.style().objectName()
noctopus     = noctopus_main.NMainWindow(currentStyle)
sys.exit(noctopusApp.exec_())
