import  subprocess
#import  re
import  platform
#import  collections
import  os
from threading import Thread
from queue import Queue, Empty


#from    PyQt5.QtGui    import QPixmap
#from    PyQt5.QtCore   import (
#    QObject,
#    QThread,
#    Qt,
#    pyqtSignal
#)

class Rrd4j(object):
    def __init__(self):
        curdir = os.path.dirname(__file__)
        classpath  = os.path.join(curdir, 'java_lib', '*') + ';'
        print(classpath)

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
        print("have read " + line)
        
    
# class Rrd4jReadThread(Thread):
#     def __init__(self, p):
#         super().__init__()
#         print("init thread?")
#         self._stdout = p
#     
#     def run(self):
#         print("run thread?")
#         while True:
#             print("try read")
#             line = self._stdout.readline()
#             print("have read" + line + " from thread!")
#         print("end run")
#         
#         self._rrdProcess.stdin.write(command)
#         responce = dict()
#         responce['cmd']     = command
#         responce['string']  = ''
#         responce['status']  = None
#         while True:
#             line = self._rrdProcess.stdout.readline()
#             if self._endOfCommandRe.match(line) == None:


# def start(parent):
#     if platform.system() == 'Windows':
#         executable = 'c:/Program Files/RRDTool/rrdtool.exe'
#     else:
#         executable = 'rrdtool'
#     Rrdtool(parent, executable)
#     
# def stop():
#     Rrdtool.singleton.shutDown()
# 
# def cmd(command, callback=None, special=None, data=None):
#     msg = dict()
#     msg['callback'] = callback
#     msg['command']  = command
#     msg['special']  = special
#     msg['data']     = data
#     Rrdtool.singleton.cmd(msg)
# 
# class Rrdtool(QObject):
#     def __init__(self, parent=None, executable='rrdtool'):
#         super(Rrdtool, self).__init__(parent)
#         Rrdtool.singleton = self
#         self._executable    = executable
#         self._threadList    = []
#         self._rrdExeList    = []
#         self._signalList    = collections.deque()
# 
#         threadCount         = QThread.idealThreadCount()
#         if isinstance(threadCount, int):
#             if threadCount == -1:
#                 self._addRrdThread()
#             else:
#                 for i in range(threadCount):
#                     self._addRrdThread()
#         else:
#             return False
# 
#     def _addRrdThread(self):
#         sig     = RrdpyqtSignal(self)
#         thread  = QThread(self)
#         rrdexe  = RrdtoolThread(self._executable)
#         rrdexe.moveToThread(thread)
#         thread.start()
#         rrdexe.uppyqtSignal.connect(self.getReply, Qt.QueuedConnection)
#         sig.downpyqtSignal.connect(rrdexe.cmd, Qt.QueuedConnection)
# 
#         self._threadList.append(thread)
#         self._signalList.append(sig)
#         self._rrdExeList.append(rrdexe)
# 
#     def cmd(self, msg):
#         self._signalList[0].downpyqtSignal.emit(msg)
#         self._signalList.rotate(1)
# 
#     def getReply(self, msg):
#         callback = msg['callback']
#         if callback != None: callback(msg)
# 
#     def shutDown(self):
#         for thread in self._threadList:
#             thread.quit()
#             if (thread.wait(5000) != True):
#                 thread.terminate()
#                 if (thread.wait(5000) != True):
#                     print("failed to close a norrd thread")
# 
# 
# 
# class RrdpyqtSignal(QObject):
#     downpyqtSignal = pyqtSignal(dict)
# 
# 
# class RrdtoolThread(QObject):
#     uppyqtSignal = pyqtSignal(dict)
#     def __init__(self, executable, parent=None):
#         super(RrdtoolThread, self).__init__(parent)
#         self._executable        = executable
#         self._endOfCommandRe    = re.compile('^OK.*|^ERROR.*')
#         self._okReturnRe        = re.compile('^OK.*')
#         self._includeNewlineRe  = re.compile('.*\n$')
# 
#         if platform.system() == 'Windows':
#             customStartupinfo = subprocess.STARTUPINFO()
#             customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#             self._rrdProcess = subprocess.Popen(
#                 [executable, '-'],
#                 universal_newlines=True,
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE,
#                 startupinfo=customStartupinfo
#             )
#         else:
#             self._rrdProcess = subprocess.Popen(
#                 [executable, '-'],
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE
#             )
# 
#     def cmd(self, cmd):
#         command = cmd['command']
#         reply   = self._rrdtoolExec(command)
#         cmd['reply'] = reply
# 
#         special = cmd['special']
#         if special == 'returnPixmap':
#             pixFile = cmd['data']
#             cmd['data']  = QPixmap(pixFile)
# 
#         self.uppyqtSignal.emit(cmd)
# 
#     def _rrdtoolExec(self, command):
#         if self._includeNewlineRe.match(command) == None: command += '\n'
#         self._rrdProcess.stdin.write(command)
#         responce = dict()
#         responce['cmd']     = command
#         responce['string']  = ''
#         responce['status']  = None
#         while True:
#             line = self._rrdProcess.stdout.readline()
#             if self._endOfCommandRe.match(line) == None:
#                 responce['string'] += line
#             else:
#                 responce['string'] += line
#                 if self._okReturnRe.match(line) == None:
#                     responce['status'] = 'error'
#                 else:
#                     responce['status'] = 'ok'
#                 break
#         #print("reply is: ", responce['string'])
#         return responce
