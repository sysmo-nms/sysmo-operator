#!/usr/bin/env python

from    PySide.QtGui    import QApplication
from    PySide.QtCore   import QSettings, QTranslator
import  sys
import  re
import  platform
import  noctopus_main
import  noctopus_colors


osType           = platform.platform()
noctopusSettings = QSettings("Noctopus NMS", "noctopus-client")
noctopusStyle    = noctopusSettings.value("NMainWindow/style")
noctopusTheme    = noctopusSettings.value("NMainWindow/theme")

if noctopusStyle == None:
    if   re.match('^Windows-XP..*',    osType) != None:
        noctopusStyle = 'plastique'
    elif re.match('^Linux..*',         osType) != None:
        noctopusStyle = 'plastique'
    elif re.match('^Windows-Vista..*', osType) != None: pass # native
    elif re.match('^Windows-7..*',     osType) != None: pass # native
    elif re.match('^Windows-8..*',     osType) != None: pass # native
    elif re.match('^Mac..*',           osType) != None: pass # native

print "noctopus%sstyle" % noctopusStyle
print "noctopus theme", noctopusTheme

if      noctopusStyle == None:      pass
elif    noctopusStyle == 'native':  pass
else:
    QApplication.setStyle(noctopusStyle)

    if      noctopusTheme == None:      pass
    elif    noctopusTheme == 'native':  pass
    else:
        colorPalette = noctopus_colors.getPalette(noctopusTheme)
        QApplication.setPalette(colorPalette)

translator   = QTranslator()
translator.load('fr_FR')

noctopusApp  = QApplication(sys.argv)
noctopusApp.installTranslator(translator)

currentStyle = noctopusApp.style().objectName()
noctopus     = noctopus_main.NMainWindow(currentStyle)

sys.exit(noctopusApp.exec_())
