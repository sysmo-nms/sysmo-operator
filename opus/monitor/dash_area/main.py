from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    noctopus_widgets    import NFrame

class DashContainer(NFrame):
    def __init__(self, parent):
        super(DashContainer, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setContentsMargins(6,4,2,4)
