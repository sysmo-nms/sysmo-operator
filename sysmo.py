if '__file__' not in locals():
    import platform
    import os
    if platform.system() == 'Windows':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Sysmo\\Sysmo Core", 0, winreg.KEY_READ)
        installLoc ,_  = winreg.QueryValueEx(key, "installLocation")
        winreg.CloseKey(key)
        operatorPath = os.path.join(installLoc, 'sysmo-operator')
        os.chdir(operatorPath)
        platformPluginsDir = os.path.join(operatorPath, 'plugins', 'platforms')
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platformPluginsDir
    if platform.system() == 'Linux': pass

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
