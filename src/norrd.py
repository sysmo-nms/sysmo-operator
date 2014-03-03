import  subprocess
import  re
import  platform

def init(executable='rrdtool'):
    return Rrdtool(executable)

def cmd(command):
    while True:
        ret = Rrdtool.singleton._cmd(command)
        if ret != 'busy': break

    return ret

class Rrdtool(object):
    def __init__(self, executable):
        Rrdtool.singleton = self
        self._locked            = False
        self._endOfCommandRe    = re.compile('^OK.*|^ERROR.*')
        self._okReturnRe        = re.compile('^OK.*')
        self._includeNewlineRe  = re.compile('.*\n$')
        self._initialize(executable)

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
        if self._locked == True:
            return 'busy'
        else:
            self._locked = True

        if self._includeNewlineRe.match(command) == None: command += '\n'

        Rrdtool.singleton._rrdProcess.stdin.write(command)
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

        self._locked = False
        return responce
