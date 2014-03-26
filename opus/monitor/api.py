import    opus.monitor.proxy

def connectToEvent(eventType, pyCallable):
    opus.monitor.proxy.ChanHandler.singleton.masterSignalsDict[eventType].signal.connect(pyCallable)
