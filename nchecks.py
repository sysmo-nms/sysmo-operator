from PyQt5.QtCore import QObject, Qt
from sysmo_widgets import NTemporaryFile
import supercast.main as supercast
import xml.etree.ElementTree as ET
import sys

def pr(val):
    print(val)
    sys.stdout.flush()

def start(parent):
    NChecksDefinition(parent)

def getGraphSpecsFor(check):
    NChecksDefinition.singleton.getGraphSpecFor(check)

def getFlagSpecFor(check):
    NChecksDefinition.singleton.getFlagSpecFor(check)

def getDescrFor(check):
    NChecksDefinition.singleton.getDescrFor(check)

class NChecksDefinition(QObject):
    def __init__(self, parent=None):
        super(NChecksDefinition, self).__init__(parent)
        NChecksDefinition.singleton = self
        self._fetchInfos()

    def _fetchInfos(self):
        xmlFile = NTemporaryFile(self)
        self._defFileName = xmlFile.fileName()
        request = dict()
        request['url'] = 'nchecks/all.xml'
        request['callback'] = self._handleAllCheckReply
        request['outfile'] = self._defFileName
        supercast.requestUrl(request)

    def _handleAllCheckReply(self, reply):
        outfile = reply['outfile']
        tree    = ET.parse(outfile)
        root    = tree.getroot()
        checks  = root.find('checks')
        self._checks = dict()
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

    def _handleCheckDefReply(self, reply):
        name    = reply['opaque']
        outfile = reply['outfile']
        tree    = ET.parse(outfile)
        self._checks[name]['initialized'] = True
        self._checks[name]['def'] = tree
        pr("tree is: " + str(tree))

        for i in self._checks.keys():
            if self._checks[i]['initialized'] != True: return

    def getGraphSpecFor(self, check):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'performances':
                for pchild in child:
                    if pchild.tag == 'graphs':
                        return pchild

    def getDescrFor(self, check):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'descr':
                return child.text

    def getFlagSpecFor(self, check):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'flags_def':
                return child
