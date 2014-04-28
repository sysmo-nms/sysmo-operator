import  opus.monitor.proxy
import  opus.monitor.trees_area.tree_probes.main
import  opus.monitor.norrd

def connectToEvent(eventType, pyCallable):
    "Connect to events emited by the server."
    opus.monitor.proxy.ChanHandler.singleton.masterSignalsDict[eventType].signal.connect(pyCallable)

def getProbeSelection():
    "Return a list of probes actualy selected in the left tree view"
    singleton = opus.monitor.trees_area.tree_probes.main.ProbesTreeview.singleton
    return singleton.getSelectedElements()

def rrdCmd(cmd, pyCallable=None):
    opus.monitor.norrd.cmd(cmd, pyCallable)

def getTargetsDict():
    return opus.monitor.proxy.ChanHandler.singleton.targets


def getProbesDict():
    return opus.monitor.proxy.ChanHandler.singleton.probes
