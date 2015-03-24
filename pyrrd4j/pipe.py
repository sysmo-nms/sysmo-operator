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

class Rrd4jAsync(QObject):
    def __init__(self, parent, colorCommand):
        super(Rrd4jAsync, self).__init__(parent)
        Rrd4jAsync.singleton = self
        self._queries = dict()
        curdir = os.path.dirname(__file__)
        classpath  = os.path.join(curdir, 'java_lib', '*') + ';'

        if platform.system() == 'Windows':
            command = ["javaw", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
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
        self._setConfig(colorCommand)

    def _setConfig(self, colorCommand):
        cfgC = dict()
        cfgC['callback'] = self._setConfigReply
        cfgC['string'] = colorCommand
        self.execute(cfgC)

    def _setConfigReply(self, msg): pass
        #print("seconfigreply: " + msg)
    

    def execute(self, command):
        queryId = self._getQueryId(command['callback'])
        cmdString = "%i:%s" % (queryId, command['string'])
        self._rrd4jProcess.stdin.write(cmdString + '\n')
        self._rrd4jProcess.stdin.flush()

    def _handleReply(self, msg):
        reply = msg.split(':', 1)
        replyId     = reply[0]
        replyIdInt  = int(replyId)
        replyMsg    = reply[1]
        callback = self._queries[replyIdInt]
        del self._queries[replyIdInt]
        callback(replyMsg.rstrip())

    def _getQueryId(self, pyCallable):
        queryId = 0
        while True:
            if queryId not in self._queries:
                self._queries[queryId] = pyCallable
                return queryId
            else:
                queryId = queryId + 1

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



# class Rrd4jSimple(object):
#     def __init__(self):
#         object.__init__(self)
#         curdir = os.path.dirname(__file__)
#         classpath  = os.path.join(curdir, 'java_lib', '*') + ';'
# 
#         if platform.system() == 'Windows':
#             command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
#             customStartupinfo = subprocess.STARTUPINFO()
#             customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#             self._rrd4jProcess = subprocess.Popen(
#                 command, 
#                 universal_newlines=True,
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE,
#                 startupinfo=customStartupinfo
#             )
#         else:
#             command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
#             self._rrd4jProcess = subprocess.Popen(
#                 command,
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE
#             )
# 
#     def execute(self, msg):
#         print("write stdin: " + msg)
#         msg += '\n'
#         self._rrd4jProcess.stdin.write(msg)
#         line = self._rrd4jProcess.stdout.readline()
#         print("read stdout: " + line)
# 
