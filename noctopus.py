# python lib
import  sys
import  re
import  platform
from PySide.QtGui       import QApplication
import noctopus_main
import noctopus_api


if __name__ == '__main__':

    osType = platform.platform()
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
    noctopus.setWindowIcon(noctopus_api.nGetIcon('applications-development'))
    sys.exit(noctopusApp.exec_())
