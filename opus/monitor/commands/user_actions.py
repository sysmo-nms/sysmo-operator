from PySide.QtCore import (
    QObject,
    QSettings,
    Signal
)
from PySide.QtGui import (
    QDialog,
    QLabel,
    QListWidget
)
from noctopus_widgets import (
    NGrid,
    NGridContainer
)

import nocapi
import shlex
import re
import subprocess
import opus.monitor.proxy

# TODO possibilite de:
# - declancher un evenement lors de l'execution d'une action.
# Sera logguee sur le serveur.
# ET/OU
# - declancher une action serveur via api locale, pour executer une commande
# serveur. Exemple, ouverture d'un terminal [...] fermeture du terminal
# et sauvegarde eventuelle de configuration sur un element (action serveur)

class UserActions(QObject):
    
    signal = Signal()

    def __init__(self, parent=None):
        super(UserActions, self).__init__(parent)
        self._settings = QSettings()
        UserActions.singleton = self
        #self._createConfExample()
        nocapi.nConnectWillClose(self._saveSettings)
        self._loadSettings()

    def getUActionsFor(self, element):
        if element in self._UACfg.keys():
            return self._UACfg[element]
        else:
            return []
            
    def execUAction(self, action, target):
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

    def getUActionsCmds(self):
        return self._UACmds

    def _getTargetsDict(self):
        return opus.monitor.proxy.ChanHandler.singleton.targets

    def _loadSettings(self):
        self._UACmds = self._settings.value('monitor/user_actions_cmds')
        self._UACfg  = self._settings.value('monitor/user_actions_cfg')

    def _saveSettings(self):
        self._settings.setValue('monitor/user_actions_cmds', self._UACmds)
        self._settings.setValue('monitor/user_actions_cfg',  self._UACfg)
        print "will close"

    def addTargetAction(self, action, target):
        if target in self._UACfg.keys():
            actionList = self._UACfg[target]
            actionList.append(action)
            self._UACfg[target] = actionList
        else:
            self._UACfg[target] = [action]


    def _createConfExample(self):
        binds = dict()
        binds['ip']      = '<IP>'
        execLine         = ''' xterm -e 'echo "connect to device..."; ssh root@<IP>' '''

        command          = dict()
        command['cmd']   = execLine
        command['binds'] = binds

        commandDb = dict()
        commandDb['Access SSH'] = command
        self._settings.setValue('monitor/user_actions_cmds', commandDb)

        config = dict()
        config['target-1021653'] = ['Access SSH']
        config['target-146610']  = ['Access SSH']
        config['target-902996']  = ['Access SSH']
        config['target-501661']  = ['Access SSH']
        self._settings.setValue('monitor/user_actions_cfg', config)
