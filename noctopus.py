#!/usr/bin/env python

from    PyQt4.QtGui    import QApplication
from    PyQt4.QtCore   import QSettings, QTranslator
import  sys
import  re
import  platform
import  noctopus_main
import  noctopus_colors


def main():
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
    
    # TOPYQT ERROR BEGIN
    # force dark plastique
    noctopusStyle = 'plastique'
    noctopusTheme = 'dark'
    # TOPYQT ERROR END

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
    noctopusApp.setOrganizationName("Noctopus NMS")
    noctopusApp.setOrganizationDomain("noctopus-nms.com")
    noctopusApp.setApplicationName("noctopus-client")
    
    currentStyle = noctopusApp.style().objectName()
    noctopus     = noctopus_main.NMainWindow(currentStyle)
    
    sys.exit(noctopusApp.exec_())

# import profile
# import pstats
# profile.run('import noctopus_main; main()', 'profile.tmp')
# p = pstats.Stats('profile.tmp')
# p.sort_stats('time', 'cum').print_stats(10)
# p.print_callers('norrd')
# p.sort_stats('call').print_stats('norrd')
main()
