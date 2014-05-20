from PySide.QtCore import (
    QObject,
    QSettings
)
from PySide.QtGui import (
    QDialog,
    QLabel
)
from noctopus_widgets import (
    NGrid,
    NGridContainer
)

# TODO possibilité de déclancher un évènement lors de l'execution d'une
# action. Sera logguée sur le serveur.
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
        grid.addWidget(QLabel('hello user action', self), 0,0)
        self.setLayout(grid)
