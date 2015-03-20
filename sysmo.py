import os
if '__file__' in locals(): pass
else:
    platformPluginsDir = os.getcwd() + '\plugins\platforms'
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platformPluginsDir

from    PyQt5.QtWidgets import QApplication
from    PyQt5.QtCore    import QSettings, QTranslator
import  sys
import  sysmo_main
import  sysmo_colors

DEFAULT_PALETTE = 'dark'

QApplication.setStyle('fusion')
sysmoSettings   = QSettings("Sysmo Monitor", "sysmo-operator")
sysmoTheme      = sysmoSettings.value("NMainWindow/theme")

if (sysmoTheme == None):
   sysmoTheme = DEFAULT_PALETTE

if (sysmoTheme != 'native'):
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
