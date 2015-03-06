import monitor.proxy
import monitor.gui.tree
import monitor.norrd
import monitor.user_operations

def connectToEvent(eventType, pyCallable):
    "Connect to events emited by the server."
    monitor.proxy.ChanHandler.singleton.masterpyqtSignalsDict[eventType].signal.connect(pyCallable)

def getProbeSelection():
    "Return a list of probes actualy selected in the left tree view"
    singleton = monitor.gui.tree.ProbesTreeview.singleton
    return singleton.getSelectedElements()

def rrdCmd(cmd, pyCallable=None):
    monitor.norrd.cmd(cmd, pyCallable)

def getTargetsDict():
    return monitor.proxy.ChanHandler.singleton.targets

def getTarget(target):
    return monitor.proxy.ChanHandler.singleton.targets[target]

def getProbesFor(target):
    probes = monitor.proxy.ChanHandler.singleton.probes
    probeList = list()
    for key in probes.keys():
        probe = probes[key]
        if  probe['target'] == target: probeList.append(probe)
    return probeList

def getProbesDict():
    return monitor.proxy.ChanHandler.singleton.probes

def connectToUOperationSettings(pyCallable):
    ua = monitor.user_operations.UserOperations.singleton
    ua.uactionsSettings.connect(pyCallable)

def addTargetOperation(action, target):
    ua = monitor.user_operations.UserOperations.singleton
    ua.addTargetOperation(action, target)

def getUOperationsFor(element):
    ua = monitor.user_operations.UserOperations.singleton
    return ua.getUOperationsFor(element)

def getUOperationsCmds():
    sin = monitor.user_operations.UserOperations.singleton
    cmd = sin.getUOperationsCmds()
    return cmd

def execUOperation(action, target):
    ua = monitor.user_operations.UserOperations.singleton
    return ua.execUOperation(action, target)
