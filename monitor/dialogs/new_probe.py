from PyQt5.QtWidgets import QWizard, QWizardPage
import sysmo_main
import nchecks
#from sysmo_widgets import NGrid
#import supercast.main as supercast
#from sysmo_widgets import NTemporaryFile
#import xml.etree.ElementTree as ET

class NewProbe(QWizard):
    def __init__(self, target, parent=None):
        # give parent the QMainWindow to open at the center of it
        parent = sysmo_main.NMainWindow.singleton
        super(NewProbe, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setModal(True)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)

        self._probesDict = nchecks.getProbesDef()
        print("hellow + " + str(self._probesDict))
        self.setPage(1, ProbeSelectionPage(target, self))
        self.setStartId(1)

class ProbeSelectionPage(QWizardPage):
    def __init__(self, target, parent):
        super(ProbeSelectionPage, self).__init__(parent)
        self.setTitle('New probe for target %s' % target)
        self.setSubTitle('Select a probe from the following list')
        

# class NewProbe2(QDialog):
#     def __init__(self, target, parent = None):
#         super(NewProbe2, self).__init__(parent)
#         self._initLayout()
#         self._progress = QProgressDialog(self)
#         self._fetchInfos()
#         self._target = target
# 
#     def _initLayout(self):
#         area = QAbstractScrollArea(self)
#         mgrid   = NGrid(self)
#         mgrid.addWidget(area)
#         self._cgrid = NGrid(area)
# 
#         
#     def _finalizeLayout(self):
#         self._buttons = list()
#         for key in self._checks.keys():
#             x = self._checks[key]['def']
#             y = x.find('descr')
#             b = QCommandLinkButton(key, y.text, self) 
#             b.setFixedHeight(50)
#             self._cgrid.addWidget(b)
#         
#         
#     def _fetchInfos(self):
#         self._progress.setMinimum(0)
#         self._progress.setMaximum(0)
#         self._progress.setLabelText('Fetching checks list...')
#         self._progress.setModal(True)
#         self._progress.setValue(1)
#         self._progress.show()
# 
#         xmlFile = NTemporaryFile(self)
#         self._defFileName = xmlFile.fileName()
#         request = dict()
#         request['url'] = 'nchecks/all.xml'
#         request['callback'] = self._handleAllCheckReply
#         request['outfile'] = self._defFileName
#         supercast.requestUrl(request)
# 
#     def _handleAllCheckReply(self, reply):
#         outfile= reply['outfile']
#         tree    = ET.parse(outfile)
#         root    = tree.getroot()
#         checks  = root.find('checks')
#         self._checks = dict()
#         self._progress.setLabelText('Updating check definitions...')
#         for check in checks:
#             name = check.attrib['name']
#             self._checks[name] = dict()
#             self._checks[name]['initialized'] = False
#             request = dict()
#             request['url']      = 'nchecks/%s.xml' % name
#             request['outfile']  = NTemporaryFile(self).fileName()
#             request['callback'] = self._handleCheckDefReply
#             request['opaque']   = name
#             supercast.requestUrl(request)
#         self._progress.setMaximum(len(self._checks))
# 
#     def _handleCheckDefReply(self, reply):
#         name    = reply['opaque']
#         self._progress.setLabelText('Updating %s definition...' % name)
#         print("handle check,", name)
#         self._progress.setValue(self._progress.value() + 1)
#         outfile = reply['outfile']
#         tree    = ET.parse(outfile)
#         self._checks[name]['initialized'] = True
#         self._checks[name]['def'] = tree
# 
#         for i in self._checks.keys():
#             if self._checks[i]['initialized'] != True: return
# 
#         self._progress.hide()
#         self._progress.deleteLater()
#         self._finalizeLayout()
#         self.show()
