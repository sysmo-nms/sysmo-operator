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

# TODO possibilite de:
# - declancher un evenement lors de l'execution d'une action.
# Sera logguee sur le serveur.
# ET/OU
# - declancher une action serveur via api locale, pour executer une commande
# serveur. Exemple, ouverture d'un terminal [...] fermeture du terminal
# et sauvegarde eventuelle de configuration sur un element (action serveur)

class UserActions(QObject):
    
    # for UI elements that will need to update themselfes on config move
    uactionsSettings = Signal()

    def __init__(self, parent=None):
        super(UserActions, self).__init__(parent)
        self._settings = QSettings()
        UserActions.singleton = self
        self._createConfExample()
        self._loadSettings()

    def getUActionsFor(self, target):
        if target in self._UACfg.keys():
            print "yess?"
            return self._UACfg[target]
        else:
            return []
            

    def _loadSettings(self):
        self._UACmds = self._settings.value('monitor/user_actions_cmds')
        self._UACfg  = self._settings.value('monitor/user_actions_cfg')

    def _createConfExample(self):
        binds = dict()
        binds['ip']      = '<IP>'
        execLine         = 'xterm -e "echo \"hello\"; ssh root@<IP>"'

        command          = dict()
        command['cmd']   = execLine
        command['binds'] = binds

        commandDb = dict()
        commandDb['Access SSH'] = command
        self._settings.setValue('monitor/user_actions_cmds', commandDb)

        config = dict()
        config['target-501661'] = ['Access SSH']
        config['target-952996'] = ['Access SSH']
        config['target-959975'] = ['Access SSH']
        self._settings.setValue('monitor/user_actions_cfg', config)

    def launchConfigurator(self):
        ua = UserActionsUI()
        ua.exec_()

class UserActionsUI(QDialog):
    def __init__(self, parent):
        super(UserActionsUI, self).__init__(None)
        grid = NGrid(self)
        lab = QLabel('User actions', self)
        grid.addWidget(lab, 0,0,1,4)
        self.setLayout(grid)

#         targetList      = QListWidget(self)
#         selectedTargets = QListWidget(self)
#         selectedActions = QListWidget(self)
#         actionsList     = QListWidget(self)
#         grid.addWidget(targetList,   1,0)
#         grid.addWidget(selectedTargets, 1,1)
#         grid.addWidget(selectedActions, 1,3)
#         grid.addWidget(actionsList,  1,2)
