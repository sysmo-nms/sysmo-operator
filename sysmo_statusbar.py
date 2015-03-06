from PyQt5.QtWidgets import QStatusBar

class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        #debugButton = QToolButton(self)
        #debugButton.setIcon(QIcon(getPixmap('applications-development')))
        #self.addPermanentWidget(debugButton)
