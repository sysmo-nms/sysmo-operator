from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    ModTrackerEvents    import TrackerEvents
from    TargetBody      import ElementView
import  Supercast
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile


class Stack(QStackedWidget):
    " every server events are switched to the stack concerned"
    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.stackDict  = dict()
        Stack.singleton = self
        TrackerEvents.singleton.treeviewClicked.connect(self.setView)
        TrackerEvents.singleton.unsubscribeOk.connect(self.unsubscribeOk)
        TrackerEvents.singleton.probeReturn.connect(self.handleProbeReturn)
        TrackerEvents.singleton.probeDump.connect(self.handleProbeDump)

    def setView(self, clickDict):
        # target is allready set? do nothing.
        targetName = clickDict['target']

        if targetName in self.stackDict.keys():
            self.setCurrentWidget(self.stackDict[targetName])
            return

        # should not be subscribed:
        Supercast.Link.subscribe(targetName)

        # then create the widget
        stackWidget = ElementView(self, targetName)
        self.addWidget(stackWidget)
        self.stackDict[str(targetName)] = stackWidget

        # set it current:
        self.setCurrentWidget(stackWidget)
        return

    def unsubscribeOk(self, msg):
        " these messages unstack the target specified in the msg"
        key = msg['value']
        if key in self.stackDict.keys():
            stackWidget = self.stackDict[key]
            # remove from stack
            self.removeWidget(stackWidget)
            # destroy it
            stackWidget.destroy()
            # then remove it from stackDict
            del self.stackDict[key]
        return

    def handleProbeReturn(self, msg):
        chan = msg['value']['channel']
        if chan in self.stackDict:
            self.stackDict[chan].handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        chan = msg['value']['channel']
        if chan in self.stackDict:
            self.stackDict[chan].handleProbeDump(msg)
