from PyQt5.QtCore import (
    QObject,
    QSettings,
    pyqtSignal
)
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QListWidget
)
from sysmo_widgets import (
    NGrid,
    NGridContainer
)

import sysmapi
import shlex
import re
import subprocess
import monitor.proxy

def launchOperationFor(obj, target):
    from monitor.dialogs.user_operations import UserOperationsWizard
    ua = UserOperations.singleton
    ac = ua.getUOperationsFor(target)
    if len(ac) == 0:
        uw = UserOperationsWizard(obj, target)
    else:
        action = ac[0]
        ua.execUOperation(action, target)
        
        

class UserOperations(QObject):
    
    signal = pyqtSignal()

    def __init__(self, parent=None):
        super(UserOperations, self).__init__(parent)
        self._settings = QSettings()
        UserOperations.singleton = self
        self._createConfExample()
        sysmapi.nConnectWillClose(self._saveSettings)
        self._loadSettings()

    def getUOperationsFor(self, element):
        if element in list(self._UACfg.keys()):
            return self._UACfg[element]
        else:
            return []
            
    def execUOperation(self, action, target):
        targets = self._getTargetsDict()
        tprop   = targets[target]['properties']

        cmd     = self._UACmds[action]
        line    = cmd['cmd']
        binds   = cmd['binds']
        for prop in binds:
            regx = cmd['binds'][prop]
            line = re.sub(regx, tprop[prop], line)

        args = shlex.split(line)
        subprocess.Popen(args)

    def getUOperationsCmds(self):
        return self._UACmds

    def _getTargetsDict(self):
        return monitor.proxy.ChanHandler.singleton.targets

    def _loadSettings(self):
        UACmds = self._settings.value('monitor/user_operations_cmds')
        if UACmds == None:
            self._createConfExample()
            self._UACmds = self._settings.value('monitor/user_operations_cmds')
        else:
            self._UACmds = UACmds

        UACfg = self._settings.value('monitor/user_operations_cfg')
        if UACfg == None:
            UACfg = dict()
        self._UACfg  = UACfg

    def _saveSettings(self):
        self._settings.setValue('monitor/user_operations_cmds', self._UACmds)
        self._settings.setValue('monitor/user_operations_cfg',  self._UACfg)

    def addTargetOperation(self, action, target):
        if target in list(self._UACfg.keys()):
            actionList = self._UACfg[target]
            actionList.append(action)
            self._UACfg[target] = actionList
        else:
            self._UACfg[target] = [action]


    def _createConfExample(self):
        # TODO examples:
        # . tail -f /var/log/httpd.log (avec Ctrl-C qui termine tail mais
        # ne quite pas, pour "| grep" par example)
        # . http:osinventory ("voir element", "ajouter tache")
        # . http:todolist    ("ajouter tache")
        # . reboot
        # . update ("voir check apt-get, check yum", "yum update, apt-get update")
        # . backup (ftp, git...)
        # . script auto puppet/chef/cfengine (editer -> commit git -> push -> reload conf)
        # . ./omnivista -element I (ems client)
        # . documentation (ouvrir l'explorateur de fichier client sur dossier
        # partage.
        #
        binds = dict()
        binds['ip']      = '<IP>'
        execLine         = ''' xterm -e 'echo "connect to device..."; ssh root@<IP>' '''

        command          = dict()
        command['cmd']   = execLine
        command['binds'] = binds

        commandDb = dict()
        commandDb['Access SSH'] = command
        self._settings.setValue('monitor/user_operations_cmds', commandDb)
