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

def getChecks():
    return NChecksDefinition.singleton.getChecks()

def getTableIndexInfoFor(check):
    xml_Check = NChecksDefinition.singleton.getCheck(check)
    xml_Performances = xml_Check.find('nchecks:Performances', NS)
    xml_PropertySuffix = xml_Performances.find('nchecks:PropertySuffix', NS)
    xml_PropertyPrefix = xml_Performances.find('nchecks:PropertyPrefix', NS)
    return (xml_PropertyPrefix.text, xml_PropertySuffix.text)
    
def getGraphTemplateFor(check):
    glist = list()
    xml_Check = NChecksDefinition.singleton.getCheck(check)
    xml_Performances = xml_Check.find('nchecks:Performances', NS)
    xml_GraphTable = xml_Performances.find('nchecks:GraphTable', NS)
    for xml_Graph in xml_GraphTable.findall('nchecks:Graph', NS):
        g = dict()
        xml_Title = xml_Graph.find('nchecks:Title', NS)
        xml_VerticalLabel = xml_Graph.find('nchecks:VerticalLabel', NS)
        g['title'] = xml_Title.text.strip()
        g['name'] = xml_Graph.attrib['Id']
        g['vlabel'] = xml_VerticalLabel.text.strip()
        g['maxValue'] = xml_Graph.attrib['Maximum']
        g['minValue'] = xml_Graph.attrib['Minimum']
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
            legend = xml_Draw.text.strip()
            ds.append(
                "%s,%s,%s,%s,%s" % (
                    xml_Draw.attrib['DataSource'],
                    xml_Draw.attrib['Type'],
                    legend,
                    xml_Draw.attrib['Color'],
                    xml_Draw.attrib['Consolidation']
                )
            )
        g['DS'] = ds
        glist.append(g)
    return (xml_Performances.attrib['Type'], glist)

    #pr("xml is: " + str(xml_Performances))
    
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

    def getChecks(self):
        return self._nchecks

    def getCheck(self, check):
        return self._nchecks[check]
