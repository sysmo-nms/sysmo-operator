from PyQt5.QtCore import QObject, Qt
from sysmo_widgets import NTemporaryFile
import supercast.main as supercast
import xml.etree.ElementTree as ET
import sys

def pr(val):
    print(val)
    sys.stdout.flush()

def start(parent):
    return NChecksDefinition(parent)

def getGraphTemplateFor(check):
    gdefs = NChecksDefinition.singleton.getGraphSpecFor(check)
    graphTemplates = list()
    for gdef in gdefs:
        graph = dict()
        graph['title']  = gdef.find('graphTitle').text
        graph['name']   = gdef.find('graphName').text
        graph['vlabel'] = gdef.find('verticalLabel').text
        graph['spanBegin']  = -1200
        graph['spanEnd']    = -1
        graph['width']      = 100
        graph['height']     = 50
        graph['DS']         = list()
        for ds in gdef.findall('add'):
            graph['DS'].append(
                "%s,%s,%s,%s,%s" % (
                    ds.find('name').text,
                    ds.find('graphType').text,
                    ds.find('legend').text,
                    ds.find('color').text,
                    ds.find('consolFun').text
                )
            )
        graphTemplates.append(graph)
    return graphTemplates
    

def getFlagSpecFor(check):
    return NChecksDefinition.singleton.getFlagSpecFor(check)

def getDescrFor(check):
    return NChecksDefinition.singleton.getDescrFor(check)

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

    def getGraphSpecFor(self, name):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'performances':
                for pchild in child:
                    if pchild.tag == 'graphs':
                        return pchild

    def getDescrFor(self, name):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'descr':
                return child.text

    def getFlagSpecFor(self, name):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'flags_def':
                return child
