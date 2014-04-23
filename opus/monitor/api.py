import  opus.monitor.proxy
import  opus.monitor.trees_area.tree_probes.main

def connectToEvent(eventType, pyCallable):
    "Connect to events emited by the server."
    opus.monitor.proxy.ChanHandler.singleton.masterSignalsDict[eventType].signal.connect(pyCallable)

def getProbeSelection():
    "Return a list of probes actualy selected in the left tree view"
    singleton = opus.monitor.trees_area.tree_probes.main.ProbesTreeview.singleton
    return singleton.getSelectedElements()
