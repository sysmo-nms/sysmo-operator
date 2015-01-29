# PyQt5
from    PyQt5.QtCore   import (
    pyqtSignal,
    Qt,
    QMimeData
)

from    PyQt5.QtGui    import (
    QDrag
)
from    PyQt5.QtWidgets    import (
    QPushButton
)
import noctopus_images
import noctopus_centerwidget

class NInfoButton(QPushButton):
    def __init__(self, parent=None):
        super(NInfoButton, self).__init__(parent)
        self.setIcon(noctopus_images.getIcon('dialog-information'))
        self.setFlat(True)
        self._showInfoEnabled = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStart = event.pos()
        noctopus_centerwidget.NCentralFrame.singleton.showInfo(True)
        self._showInfoEnabled = True

    def mouseMoveEvent(self, event):
        if self._showInfoEnabled == False:
            noctopus_centerwidget.NCentralFrame.singleton.showInfo(True)
            self._showInfoEnabled = True
        print("move event")
        drag = QDrag(self)
        drag.setPixmap(noctopus_images.getPixmap('system-search'))
        mime = QMimeData()
        drag.setMimeData(mime)
        drag.exec_()
        QPushButton.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
            noctopus_centerwidget.NCentralFrame.singleton.showInfo(False)
