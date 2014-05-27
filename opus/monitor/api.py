import  opus.monitor.proxy
import  opus.monitor.trees_area.tree_probes.main
import  opus.monitor.norrd
import  opus.monitor.commands.user_actions

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

# UActions
def launchUserActionsUI():
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    ua.launchConfigurator()

def connectToUActionSettings(pyCallable):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    ua.uactionsSettings.connect(pyCallable)

def getUActionsFor(target):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    return ua.getUActionsFor(target)

def execUAction(action, target):
    ua = opus.monitor.commands.user_actions.UserActions.singleton
    return ua.execUAction(action, target)
    
def getCheckInfos():
    return opus.monitor.proxy.ChanHandler.singleton.checkInfos
