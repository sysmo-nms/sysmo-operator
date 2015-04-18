from PyQt5.QtCore import QObject, Qt
from sysmo_widgets import NTemporaryFile
import supercast.main as supercast
import xml.etree.ElementTree as ET
import sys

NS = {'nchecks': 'http://schemas.sysmo.io/2015/NChecks'}

def pr(val):
    print("nchecks debug!!!!!!!!!!!!!!" + str(val))
    sys.stdout.flush()

def start(parent):
    return NChecksDefinition(parent)

def getGraphTemplateFor(check):
    glist = list()
    xml_Check = NChecksDefinition.singleton.getCheck(check)
    xml_Performances = xml_Check.find('nchecks:Performances', NS)
    xml_GraphTable = xml_Performances.find('nchecks:GraphTable', NS)
    for xml_Graph in xml_GraphTable.findall('nchecks:Graph', NS):
        g = dict()
        g['title'] = xml_Graph.attrib['Title']
        g['name'] = xml_Graph.attrib['Id']
        g['vlabel'] = xml_Graph.attrib['VerticalLabel']
        g['maxValue'] = xml_Graph.attrib['Max']
        g['minValue'] = xml_Graph.attrib['Min']
        g['rigid'] = xml_Graph.attrib['Rigid']
        g['base'] = xml_Graph.attrib['Base']
        g['unit'] = xml_Graph.attrib['Unit']
        g['unitExponent'] = xml_Graph.attrib['UnitExponent']
        g['spanBegin'] = -1200
        g['spanEnd'] = -1
        g['width'] = 600
        g['height'] = 200
        g['filenameRrd'] = None
        g['filenamePng'] = None
        ds = list()
        for xml_Draw in xml_Graph.findall('nchecks:Draw', NS):
            ds.append(
                "%s,%s,%s,%s,%s" % (
                    xml_Draw.attrib['DataSource'],
                    xml_Draw.attrib['Type'],
                    xml_Draw.attrib['Legend'],
                    xml_Draw.attrib['Color'],
                    xml_Draw.attrib['Consolidation']
                )
            )
        g['DS'] = ds
        glist.append(g)
    return (xml_Performances.attrib['Type'], glist)

    #pr("xml is: " + str(xml_Performances))

def getGraphTemplateFor2(check):
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
    

def getChecks():
    return NChecksDefinition.singleton.getChecks()

def getFlagSpecFor(check):
    return NChecksDefinition.singleton.getFlagSpecFor(check)

def getClassNameFor(check):
    return NChecksDefinition.singleton.getClassNameFor(check)

def getDescrFor(check):
    return NChecksDefinition.singleton.getDescrFor(check)


def getProbesDef():
    return NChecksDefinition.singleton.getProbesDef()

class NChecksDefinition(QObject):
    def __init__(self, parent=None):
        super(NChecksDefinition, self).__init__(parent)
        NChecksDefinition.singleton = self
        self._nchecks = dict()
        # get the CheckAccessTable from NChecks.xml
        xmlFile = NTemporaryFile(self)
        self._defFileName = xmlFile.fileName()
        request = dict()
        request['url'] = 'nchecks/NChecks.xml'
        request['callback'] = self._allCheckCallback
        request['outfile']  = self._defFileName
        supercast.requestUrl(request)

    def _allCheckCallback(self, reply):
        xml_NChecks = ET.parse(reply['outfile']).getroot()
        xml_CheckAccessTable = xml_NChecks.find('nchecks:CheckAccessTable', NS)
        for xml_CheckUrl in xml_CheckAccessTable.findall('nchecks:CheckUrl', NS):
            name  = xml_CheckUrl.attrib['Id']
            xfile = xml_CheckUrl.attrib['Value']
            request = dict()
            request['url']      = 'nchecks/%s' % xfile
            request['outfile']  = NTemporaryFile(self).fileName()
            request['callback'] = self._checkDefCallback
            pr(request)
            supercast.requestUrl(request)

    def _checkDefCallback(self, reply):
        xml_NChecks = ET.parse(reply['outfile']).getroot()
        xml_Check = xml_NChecks.find('nchecks:Check', NS)
        self._nchecks[xml_Check.attrib['Id']] = xml_Check

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

    def getChecks(self):
        return self._nchecks

    def getCheck(self, check):
        return self._nchecks[check]

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
                    checkDict['flag_info'] = list()
                    for flag in child.findall('flag_info'):
                        name = flag.find('name').text
                        d = dict()
                        d['name'] = flag.find('name').text
                        d['usage'] = flag.find('usage').text
                        d['default'] = flag.find('default').text
                        d['role'] = flag.find('role').text
                        d['type'] = flag.find('type').text
                        d['hint'] = flag.find('hint').text
                        checkDict['flag_info'].append(d)
                
            replyDict[key] = checkDict
        return replyDict

    def getClassNameFor(self, name):
        root = self._checks[name]['def'].getroot()
        for child in root:
            if child.tag == 'probe_class':
                return child.text
