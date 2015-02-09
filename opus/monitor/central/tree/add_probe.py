#from    PyQt5.QtGui        import QIcon
from    PyQt5.QtWidgets    import (
    #QToolBox,
    QDialog,
    QProgressDialog
    #QWidget,
    #QLabel,
    #QFrame,
    #QGridLayout,
    #QListView,
    #QListWidget,
    #QListWidgetItem,
    #QAbstractItemView,
    #QStackedWidget,
    #QPushButton
)

#from    PyQt5.QtCore   import QSettings, QSize, Qt
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid
)

import supercast.main as supercast
from noctopus_widgets import NTemporaryFile
import xml.etree.ElementTree as ET
#import  nocapi
#import  opus.monitor.api    as monapi


class AddProbe(QDialog):
    def __init__(self, target, parent = None):
        super(AddProbe, self).__init__(parent)
        self._progress = QProgressDialog(self)
        self._fetchInfos()
        self._target = target

    def _fetchInfos(self):
        self._progress.setMinimum(0)
        self._progress.setMaximum(0)
        self._progress.setLabelText('Fetching checks list...')
        self._progress.setModal(True)
        self._progress.setValue(1)
        self._progress.show()

        xmlFile = NTemporaryFile(self)
        self._defFileName = xmlFile.fileName()
        request = dict()
        request['url'] = 'nchecks/all.xml'
        request['callback'] = self._handleAllCheckReply
        request['outfile'] = self._defFileName
        supercast.requestUrl(request)

    def _handleAllCheckReply(self, reply):
        outfile= reply['outfile']
        tree    = ET.parse(outfile)
        root    = tree.getroot()
        checks  = root.find('checks')
        self._checks = dict()
        self._progress.setLabelText('Updating check definitions...')
        for check in checks:
            name = check.attrib['name']
            self._checks[name] = dict()
            self._checks[name]['initialized'] = False
            request = dict()
            request['url']      = 'nchecks/%s.xml' % name
            request['outfile']  = NTemporaryFile(self).fileName()
            request['callback'] = self._handleCheckDefReply
            request['opaque']   = name
            supercast.requestUrl(request)
        self._progress.setMaximum(len(self._checks))

    def _handleCheckDefReply(self, reply):
        name    = reply['opaque']
        self._progress.setLabelText('Updating %s definition...' % name)
        print("handle check,", name)
        self._progress.setValue(self._progress.value() + 1)
        outfile = reply['outfile']
        tree    = ET.parse(outfile)
        self._checks[name]['initialized'] = True
        self._checks[name]['def'] = tree

        for i in self._checks.keys():
            if self._checks[i]['initialized'] != True: return

        self._progress.hide()
        self._progress.deleteLater()
        self.show()














