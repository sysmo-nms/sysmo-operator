from    PyQt5.QtWidgets    import (
    QToolBox,
    QDialog,
    QWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QListView,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QStackedWidget,
    QPushButton
)

from    PyQt5.QtCore   import QSettings, QSize, Qt
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid,
    QLabel
)

import  nocapi
import  opus.monitor.api    as monapi

def openTargetPropertiesFor(target):
    if target not in list(TargetProperties.Elements.keys()):
        v = TargetProperties(target)
        TargetProperties.Elements[target] = v
    else:
        TargetProperties.Elements[target].show()

def openProbePropertiesFor(target):
    if target not in list(ProbeProperties.Elements.keys()):
        v = ProbeProperties(target)
        ProbeProperties.Elements[target] = v
    else:
        ProbeProperties.Elements[target].show()
        

class TargetProperties(QDialog):
    Elements = dict()
    def __init__(self, element, parent = None):
        super(TargetProperties, self).__init__(parent)
        
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(450)
        layout = QGridLayout(self)
        self._confList = QListWidget(self);
        self._confList.setViewMode(QListView.IconMode)
        self._confList.setIconSize(QSize(70,70))
        self._confList.setMovement(QListView.Static)
        self._confList.setMaximumWidth(120)
        self._confList.setSpacing(12)
        self._confList.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        #p1 = TargetPropertiesP1(self)
        p1 = TargetPropertiesP1(self)
        p2 = TargetPropertiesP2(self)
        p3 = TargetPropertiesP3(self)
        p4 = TargetPropertiesP4(self)
        p5 = TargetPropertiesP5(self)
        p6 = TargetPropertiesP6(self)

        self._stack = QStackedWidget(self)
        self._stack.addWidget(p1)
        self._stack.addWidget(p2)
        self._stack.addWidget(p3)
        self._stack.addWidget(p4)
        self._stack.addWidget(p5)
        self._stack.addWidget(p6)
    
        close = QPushButton('Close', self)
        close.clicked.connect(self.close)
        
    
        layout.addWidget(self._confList, 0,0)
        layout.addWidget(self._stack, 0,1,1,2)
        layout.addWidget(close, 1,2)
        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,0)
        
        self.createIcons()
        self.show()

    def createIcons(self):
        confButton = QListWidgetItem(self._confList)
        confButton.setIcon(nocapi.nGetIcon('preferences-system'))
        confButton.setText('Properties')
        confButton.setTextAlignment(Qt.AlignHCenter)
        confButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        probesButton = QListWidgetItem(self._confList)
        probesButton.setIcon(nocapi.nGetIcon('satellite'))
        probesButton.setText('Probes')
        probesButton.setTextAlignment(Qt.AlignHCenter)
        probesButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        tieButton = QListWidgetItem(self._confList)
        tieButton.setIcon(nocapi.nGetIcon('utilities-terminal'))
        tieButton.setText('Operator\nAction')
        tieButton.setTextAlignment(Qt.AlignHCenter)
        tieButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        locationButton = QListWidgetItem(self._confList)
        locationButton.setIcon(nocapi.nGetIcon('internet-web-browser'))
        locationButton.setText('Location')
        locationButton.setTextAlignment(Qt.AlignHCenter)
        locationButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


        jobsButton = QListWidgetItem(self._confList)
        jobsButton.setIcon(nocapi.nGetIcon('appointment-new'))
        jobsButton.setText('Jobs')
        jobsButton.setTextAlignment(Qt.AlignHCenter)
        jobsButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        jobsButton.setFlags(Qt.NoItemFlags)

        tieButton = QListWidgetItem(self._confList)
        tieButton.setIcon(nocapi.nGetIcon('applications-system'))
        tieButton.setText('Tie scripts')
        tieButton.setTextAlignment(Qt.AlignHCenter)
        tieButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        tieButton.setFlags(Qt.NoItemFlags)

        self._confList.currentItemChanged.connect(self._changePage)

    def _changePage(self, current, previous):
        if current == None: 
            current = previous;
        self._stack.setCurrentIndex(self._confList.row(current))
    


        
class TargetPropertiesP1(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP1, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p1', self))

class TargetPropertiesP2(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP2, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p2', self))

class TargetPropertiesP3(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP3, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p3', self))

class TargetPropertiesP4(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP4, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p4', self))

class TargetPropertiesP5(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP5, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p5', self))

class TargetPropertiesP6(NFrame):
    def __init__(self, element, parent = None):
        super(TargetPropertiesP6, self).__init__(parent)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('p6', self))

class TargetPropertiesX(QDialog):
    Elements = dict()
    def __init__(self, element, parent = None):
        super(TargetPropertiesX, self).__init__()
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
