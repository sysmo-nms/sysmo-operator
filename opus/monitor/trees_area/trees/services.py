from    PySide.QtGui    import QTreeView



class Services(QTreeView):
    def __init__(self, parent):
        super(VirtualServices, self).__init__(parent)
        self.setAnimated(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHeaderHidden(False)
