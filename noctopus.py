# python lib
import  sys
import  re
import  platform
from PySide.QtGui       import QApplication
import noctopus_main
import noctopus_api


if __name__ == '__main__':
    noctopusApp = QApplication(sys.argv)

    osType = platform.platform()
    if   re.match('^Windows-XP..*',    osType) != None:
        noctopusApp.setStyle('plastique')
    elif re.match('^Windows-Vista..*', osType) != None:
        #noctopusApp.setStyle('plastique')
        # test on vista
        pass
    elif re.match('^Windows-7..*',     osType) != None:
        #noctopusApp.setStyle('plastique')
        # test on 7
        pass

    noctopus    = noctopus_main.NMainWindow()
    noctopus.setWindowIcon(noctopus_api.nGetIcon('applications-development'))
    sys.exit(noctopusApp.exec_())
