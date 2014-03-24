# PySide
from    PySide.QtGui    import (
    QFrame,
    QGridLayout
)

class NFrameContainer(QFrame):
    " QFrame with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NFrameContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

class NGridContainer(QGridLayout):
    " QGridLayout with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NGridContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
