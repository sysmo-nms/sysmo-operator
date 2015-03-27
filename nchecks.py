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
        graph['maxValue'] = gdef.find('max').text
        graph['minValue'] = gdef.find('min').text
        graph['rigid']  = gdef.find('rigid').text
        graph['base']   = gdef.find('base').text
        graph['unit']   = gdef.find('unit').text
        graph['unitExponent']   = gdef.find('unitExponent').text
        graph['spanBegin']  = -1200
        graph['spanEnd']    = -1
        graph['width']      = 600
        graph['height']     = 200
        graph['filenameRrd'] = None
        graph['filenamePng'] = None
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


def getProbesDef():
    return NChecksDefinition.singleton.getProbesDef()

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

    def getProbesDef(self):
        replyDict = dict()
        for key in self._checks.keys():
            root = self._checks[key]['def'].getroot()
            checkDict = dict()
            for child in root:
                if child.tag == 'descr':
                    checkDict['descr'] = child.text
                elif child.tag == 'probe_class':
                    checkDict['probe_class'] = child.text 
                elif child.tag == 'flags_def':
                    checkDict['flag_info'] = dict()
                    for flag in child.findall('flag_info'):
                        name = flag.find('name').text
                        checkDict['flag_info'][name] = dict()
                        checkDict['flag_info'][name]['usage'] = flag.find('usage').text
                        checkDict['flag_info'][name]['default'] = flag.find('default').text
                        checkDict['flag_info'][name]['role'] = flag.find('role').text
                        checkDict['flag_info'][name]['type'] = flag.find('type').text
                        checkDict['flag_info'][name]['hint'] = flag.find('hint').text
                
            replyDict[key] = checkDict
        return replyDict
