# PyQt5
from    PyQt5.QtCore   import (
    pyqtSignal,
    Qt,
    QMimeData
)

from    PyQt5.QtGui    import (
    QDrag,
    QIcon
)
from    PyQt5.QtWidgets    import (
    QPushButton
)

import sysmo_images
import sysmo_centerwidget

class NInfoButton(QPushButton):
    def __init__(self, parent=None):
        super(NInfoButton, self).__init__(parent)
        self.setIcon(QIcon(sysmo_images.getPixmap('dialog-information')))
        self.setFlat(True)
        self._showInfoEnabled = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStart = event.pos()
        sysmo_centerwidget.NCentralFrame.singleton.showInfo(True)
        self._showInfoEnabled = True

    def mouseMoveEvent(self, event):
        if self._showInfoEnabled == False:
            sysmo_centerwidget.NCentralFrame.singleton.showInfo(True)
            self._showInfoEnabled = True
        print("move event")
        drag = QDrag(self)
        drag.setPixmap(sysmo_images.getPixmap('system-search'))
        mime = QMimeData()
        drag.setMimeData(mime)
        drag.exec_()
        QPushButton.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
            sysmo_centerwidget.NCentralFrame.singleton.showInfo(False)
