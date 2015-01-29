from    PyQt4.QtGui    import (
    QToolBox,
    QDialog,
    QWidget,
    QLabel
)

from    PyQt4.QtCore   import QSettings
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    QLabel
)

import  nocapi
import  opus.monitor.api    as monapi

def openTargetPropertiesFor(target):
    if target not in TargetProperties.Elements.keys():
        v = TargetProperties(target)
        TargetProperties.Elements[target] = v
    else:
        TargetProperties.Elements[target].show()

def openProbePropertiesFor(target):
    if target not in ProbeProperties.Elements.keys():
        v = ProbeProperties(target)
        ProbeProperties.Elements[target] = v
    else:
        ProbeProperties.Elements[target].show()
        
class TargetProperties(QDialog):
    Elements = dict()
    def __init__(self, element, parent = None):
        super(TargetProperties, self).__init__()
        nocapi.nConnectWillClose(self._willClose)
        self._element = element
        self.setWindowTitle(element)
        grid = NGridContainer(self)
        toolbox = QToolBox(self)
        toolbox.addItem(QLabel('item1', self), 'item1')
        toolbox.addItem(QLabel('item2', self), 'item2')
        toolbox.addItem(QLabel('item3', self), 'item3')
        toolbox.addItem(QLabel('item4', self), 'item4')
        grid.addWidget(toolbox, 0,0)
        self.setLayout(grid)
        self.show()

    def _restoreSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_properties_geometry/%s' % self._element
        geometry = settings.value(settingsString)
        if geometry != None:
            self.restoreGeometry(geometry)

    def _saveSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_properties_geometry/%s' % self._element
        settings.setValue(settingsString, self.saveGeometry())

    def _willClose(self):
        self._saveSettings()
        self.close()

    def show(self):
        self._restoreSettings()
        self.raise_()
        QDialog.show(self)

    def closeEvent(self, event):
        self._saveSettings()
        QDialog.closeEvent(self, event)

class ProbeProperties(QDialog):
    Elements = dict()
    def __init__(self, element, parent = None):
        super(ProbeProperties, self).__init__()
        self.setWindowTitle(element)
        self._element = element
        nocapi.nConnectWillClose(self._willClose)
        grid = NGridContainer(self)
        toolbox = QToolBox(self)
        toolbox.addItem(QLabel('item1', self), 'item1')
        toolbox.addItem(QLabel('item2', self), 'item2')
        toolbox.addItem(QLabel('item3', self), 'item3')
        toolbox.addItem(QLabel('item4', self), 'item4')
        grid.addWidget(toolbox, 0,0)
        self.setLayout(grid)
        self.show()

    def _restoreSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_properties_geometry/%s' % self._element
        geometry = settings.value(settingsString)
        if geometry != None:
            self.restoreGeometry(geometry)

    def _saveSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_properties_geometry/%s' % self._element
        settings.setValue(settingsString, self.saveGeometry())

    def _willClose(self):
        self._saveSettings()
        self.close()

    def show(self):
        self._restoreSettings()
        self.raise_()
        QDialog.show(self)

    def closeEvent(self, event):
        self._saveSettings()
        QDialog.closeEvent(self, event)
