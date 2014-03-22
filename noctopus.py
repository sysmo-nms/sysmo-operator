# python lib
import  sys
from PySide.QtGui       import QApplication
import noctopus.main
import noctopus.api


if __name__ == '__main__':
    noctopusApp     = QApplication(sys.argv)
    noctopus        = noctopus_main.NMainWindow()
    noctopus.setWindowIcon(noctopus_api.nGetIcon('applications-development'))
    sys.exit(noctopusApp.exec_())
