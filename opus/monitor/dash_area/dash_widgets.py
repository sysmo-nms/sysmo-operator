from    PySide.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem
)
from    PySide.QtCore       import Qt, QSize
from    noctopus_widgets    import NFrameContainer, NGridContainer
from    opus.monitor.dash_area.drop_manager import DropMan

class DashTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(DashTreeWidget, self).__init__(parent)
        self.setAnimated(True)
        self._dropMan   = DropMan.singleton
        self._dropMan.selection.connect(self.dashSelectionChanged)
        self._probes    = dict()
        self._targets   = dict()
        self.setColumnCount(2)
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)

    def setDashLabels(self, row1, row2):
        self.setHeaderLabels([row1, row2])
        
    def setItemWidgetClass(self, itemClass):
        self._itemClass = itemClass

    def dashSelectionChanged(self, selectionDict):
        if selectionDict['action'] == 'add':
            elements = selectionDict['elements']

            for element in elements.keys():
                target      = elements[element]['target']
                customClass = self._itemClass
                customWidg  = customClass(self, element)
                if customWidg.goOn  == False:
                    customWidg.destroy()
                else:

                    if target not in self._targets.keys():
                        titem = QTreeWidgetItem(self)
                        titem.setExpanded(True)
                        titem.setFlags(Qt.ItemIsEnabled)
                        titem.setText(0, target)
                        self.addTopLevelItem(titem)
                        self._targets[target] = titem
                    else:
                        titem = self._targets[target]
    
                    pitem = QTreeWidgetItem(titem)
                    pitem.setFlags(Qt.ItemIsEnabled)
                    pitem.setText(0, element)
                    self.setItemWidget(pitem, 1, customWidg)
                    titem.addChild(pitem)
    
                    self._probes[element] = pitem

    def dropEvent(self, event):
        self._dropMan.handleDropEvent(event)
        event.setDropAction(Qt.IgnoreAction)
        QTreeWidget.dropEvent(self, event)
