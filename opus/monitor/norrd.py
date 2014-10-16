import  subprocess
import  re
import  platform
import  collections
from    PySide.QtGui    import QPixmap
from    PySide.QtCore   import (
    QObject,
    QThread,
    Qt,
    Signal
)

def start(parent):
    Rrdtool(parent)
    
def stop():
    Rrdtool.singleton.shutDown()

def cmd(command, callback=None, special=None, data=None):
    msg = dict()
    msg['callback'] = callback
    msg['command']  = command
    msg['special']  = special
    msg['data']     = data
    Rrdtool.singleton.cmd(msg)

class Rrdtool(QObject):
    def __init__(self, parent=None, executable='rrdtool'):
        super(Rrdtool, self).__init__(parent)
        Rrdtool.singleton   = self
        self._executable    = executable
        threadCount         = QThread.idealThreadCount()

        if isinstance(threadCount, int):
            if threadCount == -1:
                self._launchThreads(1)
            else:
                self._launchThreads(threadCount)
        else:
            return False

    def _launchThreads(self, num):
        self._threadList    = []
        self._signalList    = collections.deque()
        for i in range(num):
            thread = QThread()
            rrdtool = RrdtoolThread(self._executable)
            rrdtool.moveToThread(thread)
            sig = RrdSignal(self)
            rrdtool.upSignal.connect(self.getReply, Qt.QueuedConnection)
            sig.downSignal.connect(rrdtool.cmd, Qt.QueuedConnection)
            rrdtool._initializeRRDPipe()
            thread.start()
            self._threadList.append(thread)
            self._signalList.append(sig)

    def getReply(self, msg):
        callback = msg['callback']
        if callback != None: callback(msg)
        
    def cmd(self, cmd):
        self._signalList[0].downSignal.emit(cmd)
        self._signalList.rotate(1)

    def shutDown(self):
        for thread in self._threadList:
            thread.quit()


class RrdSignal(QObject):
    downSignal = Signal(dict)


class RrdtoolThread(QObject):
    upSignal = Signal(dict)
    def __init__(self, executable, parent=None):
        super(RrdtoolThread, self).__init__(parent)
        self._executable        = executable
        self._endOfCommandRe    = re.compile('^OK.*|^ERROR.*')
        self._okReturnRe        = re.compile('^OK.*')
        self._includeNewlineRe  = re.compile('.*\n$')

    def _initializeRRDPipe(self):
        executable = self._executable
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

    def cmd(self, cmd):
        command = cmd['command']
        reply   = self._rrdtoolExec(command)
        cmd['reply'] = reply

        special = cmd['special']
        if special == 'returnPixmap':
            pixFile = cmd['data']
            cmd['data']  = QPixmap(pixFile)

        self.upSignal.emit(cmd)

    def _rrdtoolExec(self, command):
        if self._includeNewlineRe.match(command) == None: command += '\n'
        self._rrdProcess.stdin.write(command)
        responce = dict()
        responce['cmd']     = command
        responce['string']  = ''
        responce['status']  = None
        while True:
            line = self._rrdProcess.stdout.readline()
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
