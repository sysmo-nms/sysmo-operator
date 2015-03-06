import os
if '__file__' in locals(): pass
else:
    platformPluginsDir = os.getcwd() + '\plugins\platforms'
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platformPluginsDir

from    PyQt5.QtWidgets    import QApplication
from    PyQt5.QtCore   import QSettings, QTranslator
import  sys
import  re
import  platform
import  sysmo_main
import  sysmo_colors


osType           = platform.platform()
sysmoSettings = QSettings("Sysmo Monitor", "sysmo-operator")
sysmoStyle    = sysmoSettings.value("NMainWindow/style")
sysmoTheme    = sysmoSettings.value("NMainWindow/theme")

if sysmoStyle == None:
    if   re.match('^Windows-XP..*',    osType) != None:
        sysmoStyle = 'fusion'
    elif re.match('^Linux..*',         osType) != None:
        sysmoStyle = 'fusion'
    elif re.match('^Windows-Vista..*', osType) != None: pass # native
    elif re.match('^Windows-7..*',     osType) != None: pass # native
    elif re.match('^Windows-8..*',     osType) != None: pass # native
    elif re.match('^Mac..*',           osType) != None: pass # native

if      sysmoStyle == None:      pass
elif    sysmoStyle == 'native':  pass
else:
    QApplication.setStyle(sysmoStyle)

    if      sysmoTheme == None:      pass
    elif    sysmoTheme == 'native':  pass
    else:
        colorPalette = sysmo_colors.getPalette(sysmoTheme)
        QApplication.setPalette(colorPalette)

translator   = QTranslator()
translator.load('fr_FR')

sysmoApp  = QApplication(sys.argv)
sysmoApp.installTranslator(translator)
sysmoApp.setOrganizationName("Sysmo Monitor")
sysmoApp.setOrganizationDomain("sysmo.com")
sysmoApp.setApplicationName("sysmo-operator")

currentStyle = sysmoApp.style().objectName()
sysmo        = sysmo_main.NMainWindow(currentStyle)

sys.exit(sysmoApp.exec_())
