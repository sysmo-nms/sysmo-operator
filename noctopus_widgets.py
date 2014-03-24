# PySide
from    PySide.QtGui    import (
    QFrame,
    QGridLayout
)

class NFrame(QFrame):
    def __init__(self, parent=None):
        super(NFrame, self).__init__(parent)

class NFrameContainer(QFrame):
    " QFrame with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NFrameContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)


class NGrid(QGridLayout):
    def __init__(self, parent=None):
        super(NGrid, self).__init__(parent)

class NGridContainer(QGridLayout):
    " QGridLayout with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NGridContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
