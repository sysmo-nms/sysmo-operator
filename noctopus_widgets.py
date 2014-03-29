# PySide
from    PySide.QtSvg    import QSvgWidget
from    PySide.QtCore   import (
    Qt,
    QUrl,
    Signal
)

from    PySide.QtGui    import (
    QFrame,
    QLabel,
    QGridLayout,
    QSplitter,
    QCommandLinkButton,
    QDesktopServices,
    QPushButton
)
import noctopus_images

# SPLITER
class NSplitter(QSplitter):
    def __init__(self, parent=None):
        super(NSplitter, self).__init__(parent)
        self.setContentsMargins(2,2,2,2)

class NSplitterContainer(QSplitter):
    def __init__(self, parent=None):
        super(NSplitterContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

# FRAME
class NFrame(QFrame):
    def __init__(self, parent=None):
        super(NFrame, self).__init__(parent)
        self.setContentsMargins(2,2,2,2)

class NFrameContainer(QFrame):
    " QFrame with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NFrameContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

# GRID
class NGrid(QGridLayout):
    def __init__(self, parent=None):
        super(NGrid, self).__init__(parent)
        self.setContentsMargins(4,4,4,4)

class NGridContainer(QGridLayout):
    " QGridLayout with contents margins to 0 0 0 0 "
    def __init__(self, parent=None):
        super(NGridContainer, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

class NInfoButton(QPushButton):
    showInfo = Signal(bool)
    def __init__(self, parent=None):
        super(NInfoButton, self).__init__(parent)
        #self.showInfo.connect(noctopus_centerwidget.NCentralFrame.singleton.showInfo)
        self.setIcon(noctopus_images.getIcon('dialog-information'))
        self.setFlat(True)
        self.pressed.connect(self._showInfo)
        self.released.connect(self._hideInfo)

    def _showInfo(self):
        self.showInfo.emit(True)

    def _hideInfo(self):
        self.showInfo.emit(False)

class Community(NFrame):
    def __init__(self, parent=None):
        super(Community, self).__init__(parent)
        self.setFixedWidth(400)
        grid = NGrid(self)
        helpButton  = QCommandLinkButton(
            self.tr('Getting help'),
            self.tr('The documentation did not help you to solve your problem? You may try the forum or the mailing list!'),
            self
        )
        ideaButton  = QCommandLinkButton(
            self.tr('Submit an idea'),
            self.tr('You have an idea to improve user experience? Share it!'),
            self
        )
        bugButton   = QCommandLinkButton(
            self.tr('Submit a bug'),
            self.tr('You have found a disfonction in the interface? Please let us known...'),
            self
        )
        functionButton   = QCommandLinkButton(
            self.tr('Vote for a functionnality'),
            self.tr('Take a look at the functionnality planning and vote for the most usefull for you!'),
            self
        )
        helpButton.setIcon(noctopus_images.getIcon('help-browser'))
        helpButton.clicked.connect(self._goHelp)
        ideaButton.setIcon(noctopus_images.getIcon('dialog-information'))
        ideaButton.clicked.connect(self._goIdea)
        bugButton.setIcon(noctopus_images.getIcon('dialog-warning'))
        bugButton.clicked.connect(self._goBug)
        functionButton.setIcon(noctopus_images.getIcon('applications-system'))
        functionButton.clicked.connect(self._goFun)

        lab = QLabel('<h2>%s</h2' % self.tr('The community side'), self)
        ima = QSvgWidget(noctopus_images.getImage('face-devilish'), self)

        # layout is right to left
        grid.addWidget(ima,             0,0,1,1)
        grid.addWidget(lab,             0,2,1,1)
        grid.addWidget(helpButton,      1,0,1,3)
        grid.addWidget(ideaButton,      2,0,1,3)
        grid.addWidget(functionButton,  3,0,1,3)
        grid.addWidget(bugButton,       4,0,1,3)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,1)
        self.setLayout(grid)

    def _goHelp(self):
        url = QUrl('http://fr.wikipedia.fr')
        QDesktopServices.openUrl(url)

    def _goBug(self):
        url = QUrl('http://fr.wikipedia.fr')
        QDesktopServices.openUrl(url)

    def _goIdea(self):
        url = QUrl('http://fr.wikipedia.fr')
        QDesktopServices.openUrl(url)

    def _goFun(self):
        url = QUrl('http://fr.wikipedia.fr')
        QDesktopServices.openUrl(url)
