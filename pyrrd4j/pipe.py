import  subprocess
import  platform
import  os
import  time
import  sys
from PyQt5.QtCore import (
    QObject,
    QThread,
    Qt,
    pyqtSignal
)

def pr(v):
    print(v)
    sys.stdout.flush()

class Rrd4jAsync(QObject):
    def __init__(self, parent=None):
        super(Rrd4jAsync, self).__init__(parent)
        curdir = os.path.dirname(__file__)
        classpath  = os.path.join(curdir, 'java_lib', '*') + ';'

        if platform.system() == 'Windows':
            command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
            customStartupinfo = subprocess.STARTUPINFO()
            customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._rrd4jProcess = subprocess.Popen(
                command, 
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                startupinfo=customStartupinfo
            )
        else:
            command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
            self._rrd4jProcess = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )

        self._runsig = SimpleSignal(self)
        self._thread = QThread(self)
        self._reader = Rrd4jAsyncReader(self._rrd4jProcess.stdout)
        self._reader.moveToThread(self._thread)
        self._thread.start()
        self._runsig.signal.connect(self._reader._loop, Qt.QueuedConnection)
        self._reader.signal.connect(self._handleReply, Qt.QueuedConnection)
        self._runsig.signal.emit()
        

    def execute(self, msg):
        # TODO execute(self, callback, msg) 
        # id = getid()
        # dict {id, callback}
        # msg = JSON
        self._rrd4jProcess.stdin.write(msg + '\n')

    def _handleReply(self, msg):
        # TODO 
        # del dict {id, callback}
        # msg = JSON
        pr("it is a big reply: " + msg)


class Rrd4jAsyncReader(QObject):
    signal = pyqtSignal(str)
    def __init__(self, fd, parent=None):
        super(Rrd4jAsyncReader, self).__init__(parent)
        self._fd    = fd

    def _loop(self):
        while True:
            v = self._fd.readline()
            self.signal.emit(v)


class SimpleSignal(QObject):
    signal = pyqtSignal()
    def __init__(self, parent=None):
        super(SimpleSignal, self).__init__(parent)


class Rrd4jSimple(object):
    def __init__(self):
        object.__init__(self)
        curdir = os.path.dirname(__file__)
        classpath  = os.path.join(curdir, 'java_lib', '*') + ';'

        if platform.system() == 'Windows':
            command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
            customStartupinfo = subprocess.STARTUPINFO()
            customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._rrd4jProcess = subprocess.Popen(
                command, 
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                startupinfo=customStartupinfo
            )
        else:
            command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
            self._rrd4jProcess = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )

    def execute(self, msg):
        print("write stdin: " + msg)
        msg += '\n'
        self._rrd4jProcess.stdin.write(msg)
        line = self._rrd4jProcess.stdout.readline()
        print("read stdout: " + line)

