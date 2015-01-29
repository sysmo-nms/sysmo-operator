# python lib
from    functools       import partial
from    PyQt5.QtGui    import (
    QStatusBar,
    QToolButton
)
from    noctopus_images import getIcon

class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        debugButton = QToolButton(self)
        debugButton.setIcon(getIcon('applications-development'))
        self.addPermanentWidget(debugButton)
