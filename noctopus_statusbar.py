# python lib
from functools import partial

# PySide
from    PySide.QtGui    import (
    QStatusBar,
    QToolButton
)


# local dependencies
from    noctopus_images     import getIcon

class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        debugButton = QToolButton(self)
        debugButton.setIcon(getIcon('applications-development'))
        self.addPermanentWidget(debugButton)
