from    PySide.QtCore   import *

class TrackerEvents(QObject):

    " This class is used to connect childs modules to receive tracker signals"
    " It must be instanciated before theyre imports."
    " A module wishing to receiv such events have to: "
    " TrackerEvents.singleton.probeDump.connect(function)"

    # emited from ModTracker.TrackerMain:
    probeDump       = Signal(dict)
    probeInfo       = Signal(dict)
    targetInfo      = Signal(dict)
    probeModInfo    = Signal(dict)
    probeReturn     = Signal(dict)
    probeActivity   = Signal(dict)
    subscribeOk     = Signal(dict)
    unsubscribeOk   = Signal(dict)

    # emited from ModTrackerTreeView.TrackerTView:
    treeviewClicked = Signal(dict)

    def __init__(self, parent):
        super(TrackerEvents, self).__init__(parent)
        TrackerEvents.singleton = self
