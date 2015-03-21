import os
if '__file__' in locals(): pass
else:
    platformPluginsDir = os.getcwd() + '\plugins\platforms'
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platformPluginsDir

from    PyQt5.QtWidgets import QApplication, QWidget
from    PyQt5.QtCore    import QSettings, QTranslator
import  sys
import  sysmo_main
import  sysmo_colors

DEFAULT_PALETTE = 'dark'

QApplication.setStyle('fusion')
defaultPalette = QApplication.palette()
sysmoSettings   = QSettings("Sysmo Monitor", "sysmo-operator")
sysmoTheme      = sysmoSettings.value("NMainWindow/theme")
sysmoMenuTheme  = sysmoSettings.value("NMainWindow/menuTheme")
sysmoMenuBarTheme = sysmoSettings.value("NMainWindow/menuBarTheme")


if (sysmoTheme != None and sysmoTheme != 'native'):
    colorPalette = sysmo_colors.getPalette(sysmoTheme)
    QApplication.setPalette(colorPalette)

if (sysmoMenuBarTheme != None and sysmoMenuBarTheme != 'native'):
    QApplication.setPalette(sysmo_colors.getPalette(sysmoMenuBarTheme), "QMenuBar")

if (sysmoMenuTheme != None and sysmoMenuTheme != 'native'):
    QApplication.setPalette(sysmo_colors.getPalette(sysmoMenuTheme), "QMenu")

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
