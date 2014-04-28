from    PySide.QtCore   import QObject, Signal
import  opus.monitor.api as monapi

class DropMan(QObject):
    selection = Signal(dict)

    def __init__(self, parent):
        super(DropMan, self).__init__(parent)
        DropMan.singleton   = self
        self._selection     = list()

    def handleDropEvent(self, event):
        selection   = monapi.getProbeSelection()
        probes      = monapi.getProbesDict()
        newSelection = dict()

        for element in selection:
            if element not in self._selection:
                self._selection.append(element)
                newSelection[element] = probes[element]

        if len(newSelection) != 0:
            select = dict()
            select['action']    = 'add'
            select['elements']  = newSelection
            self.selection.emit(select)

    def handleCleanEvent(self):
        oldselect       = self._selection
        self._selection = list()
        select = dict()
        select['action']    = 'remove'
        select['elements']  = oldselect
        self.selection.emit(select)
