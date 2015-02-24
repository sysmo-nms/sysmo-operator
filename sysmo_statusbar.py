# python lib
from    functools       import partial
from    PyQt5.QtGui    import QIcon
from    PyQt5.QtWidgets    import (
    QStatusBar,
    QToolButton
)
from    sysmo_images import getIcon, getPixmap

class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        debugButton = QToolButton(self)
        debugButton.setIcon(QIcon(getPixmap('applications-development')))
        self.addPermanentWidget(debugButton)
