import  subprocess
import  platform
import  os


class Rrd4j(object):
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
