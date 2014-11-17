import  opus.monitor.proxy
import  opus.monitor.central.tree.main
import  opus.monitor.norrd
import  opus.monitor.commands.user_actions

def connectToEvent(eventType, pyCallable):
    "Connect to events emited by the server."
    opus.monitor.proxy.ChanHandler.singleton.masterSignalsDict[eventType].signal.connect(pyCallable)

def getProbeSelection():
    "Return a list of probes actualy selected in the left tree view"
    singleton = opus.monitor.central.tree.main.ProbesTreeview.singleton
    return singleton.getSelectedElements()

def rrdCmd(cmd, pyCallable=None):
    opus.monitor.norrd.cmd(cmd, pyCallable)

def getTargetsDict():
    return opus.monitor.proxy.ChanHandler.singleton.targets


def getProbesDict():
    return opus.monitor.proxy.ChanHandler.singleton.probes

def connectToUActionSettings(pyCallable):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    ua.uactionsSettings.connect(pyCallable)

def addTargetAction(action, target):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    ua.addTargetAction(action, target)

def getUActionsFor(element):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    return ua.getUActionsFor(element)

def getUActionsCmds():
    sin = opus.monitor.commands.user_actions.UserActions.singleton
    cmd = sin.getUActionsCmds()
    return cmd

def execUAction(action, target):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    return ua.execUAction(action, target)
