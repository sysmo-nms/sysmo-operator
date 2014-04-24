import  subprocess
import  re
import  platform
from    Queue       import Queue
from    threading   import Thread, Event
from    PySide.QtCore import *

def init(executable='rrdtool', parent=None):
    RrdtoolLocal(executable, parent)

def cmd(command, callback):
    msg = dict()
    msg['callback'] = callback
    msg['command']  = command
    RrdtoolLocal.singleton.send(msg)

class RrdtoolExit(Exception): pass

class RrdtoolLocal(QObject):
    def __init__(self, executable, parent=None):
        super(RrdtoolLocal, self).__init__(parent)
        RrdtoolLocal.singleton = self
        self._sendQ = Queue()
        self.rrdServer = Rrdtool(executable, self._sendQ, self)
        self.rrdServer.signal.connect(self.getReply, Qt.QueuedConnection)

        self.rrdServer.start()

    def getReply(self, msg):
        callback = msg['callback']
        if callback != None: callback(msg)
        
    def send(self, msg):
        self.rrdServer.send(msg)
        

    
class Rrdtool(QObject):
    signal = Signal(dict)
    def __init__(self, executable, sq, parent):
        super(Rrdtool, self).__init__(parent)
        self._mailbox   = sq
        Rrdtool.singleton = self
        self._endOfCommandRe    = re.compile('^OK.*|^ERROR.*')
        self._okReturnRe        = re.compile('^OK.*')
        self._includeNewlineRe  = re.compile('.*\n$')
        self._initialize(executable)

    def send(self, msg):
        self._mailbox.put(msg)

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:                self.run()
        except RrdtoolExit: pass
        finally:            self._terminated.set()

    def run(self):
        while True:
            msg = self._mailbox.get()
            message  = msg['command']
            reply    = self._cmd(message)
            msg['reply'] = reply
            self.signal.emit(msg)

    def _initialize(self, executable):
        if platform.system() == 'Windows':
            customStartupinfo = subprocess.STARTUPINFO()
            customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._rrdProcess = subprocess.Popen(
                [executable, '-'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                startupinfo=customStartupinfo
            )
        else:
            self._rrdProcess = subprocess.Popen(
                [executable, '-'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )

    def _cmd(self, command):
        if self._includeNewlineRe.match(command) == None: command += '\n'

        Rrdtool.singleton._rrdProcess.stdin.write(command)
        #TODO Rrdtool.singleton._rrdProcess.stdin.flush()
        responce = dict()
        responce['cmd']     = command
        responce['string']  = ''
        responce['status']  = None
        while True:
            line = Rrdtool.singleton._rrdProcess.stdout.readline()
            if self._endOfCommandRe.match(line) == None:
                responce['string'] += line
            else:
                responce['string'] += line
                if self._okReturnRe.match(line) == None:
                    responce['status'] = 'error'
                else:
                    responce['status'] = 'ok'
                break

        return responce
