#!/usr/bin/env python27

from    PySide.QtGui    import QApplication
from    PySide.QtCore   import QSettings
import  sys
import  re
import  platform
import  noctopus_main
import  nocapi


osType = platform.platform()

noctopusSettings = QSettings("Noctopus NMS", "noctopus-client")
noctopusStyle    = noctopusSettings.value("NMainWindow/style")

if noctopusStyle != None:
    QApplication.setStyle(noctopusStyle)
else:
    if   re.match('^Windows-XP..*',    osType) != None:
        QApplication.setStyle('plastique')
    elif re.match('^Windows-Vista..*', osType) != None:
        #QApplication.setStyle('plastique')
        # test on vista
        pass
    elif re.match('^Windows-7..*',     osType) != None:
        #QApplication.setStyle('plastique')
        # test on 7
        pass

noctopusApp = QApplication(sys.argv)
noctopus    = noctopus_main.NMainWindow()
noctopus.setWindowIcon(nocapi.nGetIcon('applications-development'))
sys.exit(noctopusApp.exec_())
