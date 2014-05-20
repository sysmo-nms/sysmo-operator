from PySide.QtCore import (
    QObject,
    QSettings
)

class UserActions(QObject):
    def __init__(self, parent=None):
        super(UserActions, self).__init__(parent)
        settings = QSettings()
