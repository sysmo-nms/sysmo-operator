from    PySide.QtCore   import Qt
from    PySide.QtGui   import (
    QGraphicsView,
    QGraphicsScene,
    QLabel,
    QPalette
)

import  nocapi

class MDIDependencies(QGraphicsView):
    def __init__(self, parent):
        super(MDIDependencies, self).__init__(parent)
        self._scene = QGraphicsScene(self)
        self._scene.setBackgroundBrush(self.palette().color(QPalette.Dark))
        self._scene.addWidget(QLabel('hello'))
        self.setScene(self._scene)

    def _addRootElement(self):
        self._scene.addWidget(QLabel('root'),wFlags=Qt.Dialog)
