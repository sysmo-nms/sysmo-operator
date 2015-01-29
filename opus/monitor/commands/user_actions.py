from PyQt4.QtCore import (
    QObject,
    QSettings,
    pyqtSignal
)
from PyQt4.QtGui import (
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
    
    signal = pyqtSignal()

    def __init__(self, parent=None):
        super(UserActions, self).__init__(parent)
        self._settings = QSettings()
        UserActions.singleton = self
        self._createConfExample()
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
        UACmds = self._settings.value('monitor/user_actions_cmds')
        if UACmds == None:
            self._createConfExample()
            self._UACmds = self._settings.value('monitor/user_actions_cmds')
        else:
            self._UACmds = UACmds

        UACfg = self._settings.value('monitor/user_actions_cfg')
        if UACfg == None:
            UACfg = dict()
        self._UACfg  = UACfg

    def _saveSettings(self):
        self._settings.setValue('monitor/user_actions_cmds', self._UACmds)
        self._settings.setValue('monitor/user_actions_cfg',  self._UACfg)

    def addTargetAction(self, action, target):
        if target in self._UACfg.keys():
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
        self._settings.setValue('monitor/user_actions_cmds', commandDb)
