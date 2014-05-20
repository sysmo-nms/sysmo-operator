from PySide.QtCore import (
    QObject,
    QSettings
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
    def __init__(self, parent=None):
        super(UserActions, self).__init__(parent)
        self._settings = QSettings()
        UserActions.singleton = self

    def launchConfigurator(self):
        ua = UserActionsUI()
        ua.exec_()

class UserActionsUI(QDialog):
    def __init__(self, parent=None):
        super(UserActionsUI, self).__init__(parent)
        grid = NGrid(self)
        lab = QLabel('User actions', self)
        targetList      = QListWidget(self)
        selectedTargets = QListWidget(self)
        selectedActions = QListWidget(self)
        actionsList     = QListWidget(self)
        grid.addWidget(lab, 0,0,1,4)
        grid.addWidget(targetList,   1,0)
        grid.addWidget(selectedTargets, 1,1)
        grid.addWidget(selectedActions, 1,3)
        grid.addWidget(actionsList,  1,2)
        self.setLayout(grid)
