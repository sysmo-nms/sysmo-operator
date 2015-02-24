import  monitor.proxy
import  monitor.central.tree.main
import  monitor.norrd
import  monitor.commands.user_actions

def connectToEvent(eventType, pyCallable):
    "Connect to events emited by the server."
    monitor.proxy.ChanHandler.singleton.masterpyqtSignalsDict[eventType].signal.connect(pyCallable)

def getProbeSelection():
    "Return a list of probes actualy selected in the left tree view"
    singleton = monitor.central.tree.main.ProbesTreeview.singleton
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

def connectToUActionSettings(pyCallable):
    ua = monitor.commands.user_actions.UserActions.singleton
    ua.uactionsSettings.connect(pyCallable)

def addTargetAction(action, target):
    ua = monitor.commands.user_actions.UserActions.singleton
    ua.addTargetAction(action, target)

def getUActionsFor(element):
    ua = monitor.commands.user_actions.UserActions.singleton
    return ua.getUActionsFor(element)

def getUActionsCmds():
    sin = monitor.commands.user_actions.UserActions.singleton
    cmd = sin.getUActionsCmds()
    return cmd

def execUAction(action, target):
    ua = monitor.commands.user_actions.UserActions.singleton
    return ua.execUAction(action, target)
