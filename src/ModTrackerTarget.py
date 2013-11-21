from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    ModTrackerEvents    import TrackerEvents
from    TargetBodyView      import TargetView
import  Supercast


class Stack(QStackedWidget):

    " every server events are switched to the stack concerned based on the "
    " targetName "

    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.stackDict  = dict()
        TrackerEvents.singleton.treeviewClicked.connect(self.setView)
        TrackerEvents.singleton.unsubscribeOk.connect(self.unsubscribeOk)
        TrackerEvents.singleton.probeReturn.connect(self.handleProbeEvent)
        TrackerEvents.singleton.probeDump.connect(self.handleProbeEvent)
        TrackerEvents.singleton.probeInfo.connect(self.handleProbeEvent)

    def setView(self, clickDict):
        targetName = clickDict['target']

        # target is allready set? do nothing but set it current
        if targetName in self.stackDict.keys():
            self.setCurrentWidget(self.stackDict[targetName]['widget'])
            return

        # should not be subscribed then subscribe
        Supercast.Link.subscribe(targetName)

        # then create the widget
        stackWidget = TargetView(self, targetName)

        # create a signal with the targetView widget as parent
        # for cleanly destroy it after a stack is destroyed
        signal      = Communicate(stackWidget)

        # set the signal handler to the widget
        stackWidget.setSignal(signal)

        # add it to the stackDict db
        self.stackDict[str(targetName)] = dict()
        self.stackDict[str(targetName)]['widget'] = stackWidget
        self.stackDict[str(targetName)]['signal'] = signal

        # add it to the stack
        self.addWidget(stackWidget)

        # and set it current:
        self.setCurrentWidget(stackWidget)
        return

    def handleProbeEvent(self, msg):
        chan = msg['value']['channel']
        if chan in self.stackDict:
            sig = self.stackDict[chan]['signal']
            sig.signal.emit(msg)

    def unsubscribeOk(self, msg):
        " these messages unstack the target specified in the msg"
        key = msg['value']
        if key in self.stackDict.keys():
            stackWidget = self.stackDict[key]['widget']
            # remove from stack
            self.removeWidget(stackWidget)
            # destroy it
            stackWidget.destroy()
            # then remove it from stackDict
            del self.stackDict[key]
        return


class Communicate(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(Communicate, self).__init__(parent)
