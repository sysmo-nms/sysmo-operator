from    PySide.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem
)
from    PySide.QtCore       import Qt, QSize
from    noctopus_widgets    import NFrameContainer, NGridContainer
from    opus.monitor.dash_area.drop_manager import DropMan
from    opus.monitor.widgets    import TextLog
import  opus.monitor.api    as monapi

class BrowserDash(NFrameContainer):
    def __init__(self, parent):
        super(BrowserDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(BrowserTree(self), 0,0)
        self.setLayout(self._grid)

class BrowserTree(QTreeWidget):
    def __init__(self, parent):
        super(BrowserTree, self).__init__(parent)
        self._dropMan   = DropMan.singleton
        self._dropMan.selection.connect(self.dashSelectionChanged)
        self._probes    = dict()
        self._targets   = dict()
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr('Elements'), self.tr('Text logs')])
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)

    def dashSelectionChanged(self, selectionDict):
        if selectionDict['action'] == 'add':
            elements = selectionDict['elements']

            for element in elements.keys():
                target = elements[element]['target']

                if target not in self._targets.keys():
                    titem = QTreeWidgetItem(self)
                    titem.setFlags(Qt.ItemIsEnabled)
                    titem.setText(0, target)
                    self.addTopLevelItem(titem)
                    self._targets[target] = titem
                else:
                    titem = self._targets[target]

                pitem = QTreeWidgetItem(titem)
                pitem.setFlags(Qt.ItemIsEnabled)
                pitem.setText(0, element)
                self.setItemWidget(pitem, 1, TextLog(self, element))
                titem.addChild(pitem)

                self._probes[element] = pitem



    def dropEvent(self, event):
        self._dropMan.handleDropEvent(event)
        event.setDropAction(Qt.IgnoreAction)
        QTreeWidget.dropEvent(self, event)
