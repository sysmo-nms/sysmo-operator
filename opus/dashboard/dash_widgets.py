from    PySide.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem,
    QFrame
)
from    PySide.QtWebKit     import *
from    PySide.QtCore       import Qt, QSize
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NGrid
)
from    opus.dashboard.drop_manager import DropMan

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

##############
# OSM WIDGET #
##############
class OSMView(NFrameContainer):
    def __init__(self, parent):
        super(OSMView, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

        self.osm    = QWebView(self)
        # XXX Found bug here. QWebView do not properly quit on application
        # shutdow when he is loading a page.
        #self.osm.load(QUrl('./html/OpenStreetMap.html'))

        self.shade = QFrame(self)
        self.shade.setAutoFillBackground(False)
        self.shade.hide()
        self._browsable = True

        self.grid = NGrid(self)
        self.grid.addWidget(self.osm, 0,0)
        self.setLayout(self.grid)

    def setBrowsable(self, bol):
        if  bol == False and self._browsable == True:
            self.shade.show()
            self.grid.addWidget(self.shade, 0,0)
            self.shadeStatus = False
        elif bol == True and self._browsable == False:
            self.shade.hide()
            self.grid.removeWidget(self.shade)
            self.shadeStatus = True
