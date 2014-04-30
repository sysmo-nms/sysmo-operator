import  subprocess
import  re
import  platform
import  collections
from    PySide.QtCore import (
    QObject,
    QThread,
    Qt,
    Signal
)

def cmd(command, callback=None):
    msg = dict()
    msg['callback'] = callback
    msg['command']  = command
    Rrdtool.singleton.cmd(msg)

class Rrdtool(QObject):
    toT1  = Signal(dict)
    toT2  = Signal(dict)
    toT3  = Signal(dict)
    toT4  = Signal(dict)
    def __init__(self, parent=None, executable='rrdtool'):
        super(Rrdtool, self).__init__(parent)
        Rrdtool.singleton = self
        self._executable  = executable

        threads = QThread.idealThreadCount()
        if   threads == 1 or threads == -1:
            self._initOne()
        elif threads == 2:
            self._initTwo()
        elif threads == 3:
            self._initThree()
        elif threads == 4:
            self._initFour()

    def _initOne(self):
        self.t1 = RrdtoolThread(self._executable, self)
        self.t1.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT1.connect(self.t1.cmd, Qt.QueuedConnection)
        self._workersLinks = collections.deque([self.toT1])
        self.t1.start()

    def _initTwo(self):
        self.t1 = RrdtoolThread(self._executable, self)
        self.t1.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT1.connect(self.t1.cmd, Qt.QueuedConnection)
        self.t2 = RrdtoolThread(self._executable, self)
        self.t2.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT2.connect(self.t2.cmd, Qt.QueuedConnection)
        self._workersLinks = collections.deque([self.toT1, self.toT2])
        self.t1.start()
        self.t2.start()

    def _initThree(self):
        self.t1 = RrdtoolThread(self._executable, self)
        self.t1.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT1.connect(self.t1.cmd, Qt.QueuedConnection)
        self.t2 = RrdtoolThread(self._executable, self)
        self.t2.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT2.connect(self.t2.cmd, Qt.QueuedConnection)
        self.t3 = RrdtoolThread(self._executable, self)
        self.t3.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT3.connect(self.t3.cmd, Qt.QueuedConnection)
        self._workersLinks = collections.deque([self.toT1, self.toT2, self.toT3])
        self.t1.start()
        self.t2.start()
        self.t3.start()

    def _initFour(self):
        self.t1 = RrdtoolThread(self._executable, self)
        self.t1.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT1.connect(self.t1.cmd, Qt.QueuedConnection)
        self.t2 = RrdtoolThread(self._executable, self)
        self.t2.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT2.connect(self.t2.cmd, Qt.QueuedConnection)
        self.t3 = RrdtoolThread(self._executable, self)
        self.t3.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT3.connect(self.t3.cmd, Qt.QueuedConnection)
        self.t4 = RrdtoolThread(self._executable, self)
        self.t4.upSignal.connect(self.getReply, Qt.QueuedConnection)
        self.toT4.connect(self.t4.cmd, Qt.QueuedConnection)
        self._workersLinks = collections.deque([self.toT1, self.toT2, self.toT3, self.toT4])
        self.t1.start()
        self.t2.start()
        self.t3.start()
        self.t4.start()

    def getReply(self, msg):
        callback = msg['callback']
        if callback != None: callback(msg)
        
    def cmd(self, cmd):
        self._workersLinks[0].emit(cmd)
        self._workersLinks.rotate(1)
        






class RrdtoolThread(QThread):
    upSignal = Signal(dict)
    def __init__(self, executable, parent):
        super(RrdtoolThread, self).__init__(parent)
        self._executable        = executable
        self._endOfCommandRe    = re.compile('^OK.*|^ERROR.*')
        self._okReturnRe        = re.compile('^OK.*')
        self._includeNewlineRe  = re.compile('.*\n$')

    def run(self):
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
        QThread.run(self)

    def cmd(self, cmd):
        command = cmd['command']
        reply   = self._rrdtoolExec(command)
        cmd['reply'] = reply
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
