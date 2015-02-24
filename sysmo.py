#!/usr/bin/env python

from    PyQt5.QtWidgets    import QApplication
from    PyQt5.QtCore   import QSettings, QTranslator
import  sys
import  re
import  platform
import  sysmo_main
import  sysmo_colors


def main():
    osType           = platform.platform()
    sysmoSettings = QSettings("Noctopus NMS", "sysmo-client")
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
    
    # TOPYQT ERROR BEGIN
    # force dark fusion
    #sysmoStyle = 'fusion'
    #sysmoTheme = 'dark'
    # TOPYQT ERROR END

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
    sysmoApp.setOrganizationName("Noctopus NMS")
    sysmoApp.setOrganizationDomain("sysmo-nms.com")
    sysmoApp.setApplicationName("sysmo-client")
    
    currentStyle = sysmoApp.style().objectName()
    sysmo     = sysmo_main.NMainWindow(currentStyle)
    
    sys.exit(sysmoApp.exec_())

# import profile
# import pstats
# profile.run('import sysmo_main; main()', 'profile.tmp')
# p = pstats.Stats('profile.tmp')
# p.sort_stats('time', 'cum').print_stats(10)
# p.print_callers('norrd')
# p.sort_stats('call').print_stats('norrd')
main()
