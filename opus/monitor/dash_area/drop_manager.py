from    PySide.QtGui   import QStandardItemModel, QStandardItem
import  opus.monitor.api as monapi

class DropModel(QStandardItemModel):
    def __init__(self, parent):
        super(DropModel, self).__init__(parent)
        self.setColumnCount(2)
        #self.setHorizontalHeaderLabels(["target/probe", "datas"]),
        DropModel.singleton = self

    def handleDropEvent(self, event):
        selection = monapi.getProbeSelection()
        print "handle drop event", selection
        for i in range(len(selection)):
            self._maybeAppendRow(selection[i])

    def _maybeAppendRow(self, element):
        self.appendRow(QStandardItem(element))
