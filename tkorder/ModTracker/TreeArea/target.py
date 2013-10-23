
class Probe(object):
    def __init__(self, probeInfoDict):
        self.channel    = probeInfoDict['channel']
        self.pid        = probeInfoDict['id']
        self.name       = probeInfoDict['name']
        self.ptype      = probeInfoDict['type']
        self.module     = probeInfoDict['probeMod']
        self.status     = probeInfoDict['status']
        self.step       = probeInfoDict['step']
        self.timeout    = probeInfoDict['timeout']
        self.infoType   = probeInfoDict['infoType']
