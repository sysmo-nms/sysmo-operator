from    PyQt4.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem,
    QFrame
)
from    PyQt4.QtWebKit     import *
from    PyQt4.QtCore       import Qt, QSize
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NGrid
)

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
