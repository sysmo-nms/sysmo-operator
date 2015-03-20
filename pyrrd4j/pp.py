import  subprocess
import  platform
import  os
import  time
import  sys
from threading import Thread


def pr(val):
    print(val)
    sys.stdout.flush()

class Rrd4jAsync(object):
    def __init__(self):
        object.__init__(self)

        r,_ = os.pipe()
        fo = os.fdopen(r)
        self._thread = RrdAsyncThread(fo)
        self._thread.start()

        curdir = os.path.dirname(__file__)
        classpath  = os.path.join(curdir, 'java_lib', '*') + ';'
        command = ["java", '-classpath', classpath, 'io.sysmo.pyrrd4j.Pyrrd4j', '--die-on-broken-pipe']
        customStartupinfo = subprocess.STARTUPINFO()
        customStartupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self._rrd4jProcess = subprocess.Popen(
            command, 
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=r,
            startupinfo=customStartupinfo
        )


    def execute(self, msg):
        pr("exec" + msg)
        msg += '\n'
        self._rrd4jProcess.stdin.write(msg)


    def waitForFinish(self):
        self._thread.join()
        pr("joined")
        
class RrdAsyncThread(Thread):
    def __init__(self, fo):
        Thread.__init__(self)
        pr("thread init" + str(fo))
        self._fd = fo

    def run(self):
        pr("thread run")
        while True:
            v = self._fd.readline()
            pr(v)
        #time.sleep(3)
        #pr("thread end run")






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

