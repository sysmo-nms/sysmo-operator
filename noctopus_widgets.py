# PyQt5
from    PyQt5.QtSvg    import QSvgWidget
from    PyQt5.QtCore   import (
    QObject,
    Qt,
    QUrl,
    pyqtSignal,
    QRegExp
)

from    PyQt5.QtGui    import (
    QRegExpValidator,
    QValidator,
    QDesktopServices
)
from    PyQt5.QtWidgets    import (
    QFrame,
    QLabel,
    QGridLayout,
    QSplitter,
    QCommandLinkButton,
    QPushButton,
    QAction,
    QLineEdit
)

import noctopus_images
import tempfile
from   functools import partial

# temporary file
class NTemporaryFile(QObject):
    def __init__(self, parent=None):
        super(NTemporaryFile, self).__init__(parent)
        self._f = tempfile.NamedTemporaryFile(prefix='noc_tmp')
        name = self._f.name
        self.destroyed.connect(partial(NTemporaryFile._deleteFile, name))
        self._f.close()

    def fileName(self):
        return self._f.name

    @staticmethod
    def _deleteFile(f):
        print(("will delete file: ", f))


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

class NMenuButton(QPushButton):
    def __init__(self, parent=None):
        super(NMenuButton, self).__init__(parent)
        self.setStyleSheet('''
            NMenuButton::menu-indicator {
                subcontrol-position: left bottom;
                subcontrol-origin:   padding;
                right: -5px;
            }
        ''')

class NInfoButton(QPushButton):
    showInfo = pyqtSignal(bool)
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

class NIpv4Validator(QRegExpValidator):
    def __init__(self, parent=None):
        super(NIpv4Validator, self).__init__(parent)
        rx = QRegExp("0*(2(5[0-5]|[0-4]\d)|1?\d{1,2})(\.0*(2(5[0-5]|[0-4]\d)|1?\d{1,2})){3}")
        self.setRegExp(rx)

class NIpv4Form(QLineEdit):
    def __init__(self, parent=None):
        super(NIpv4Form, self).__init__(parent)
        self.setPlaceholderText('example: 172.16.0.1')
        self.setValidator(NIpv4Validator(self))

class NIpv6Validator(QRegExpValidator):
    def __init__(self, parent=None):
        super(NIpv6Validator, self).__init__(parent)
        rx = QRegExp("\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*")
        self.setRegExp(rx)

class NIpv6Form(QLineEdit):
    def __init__(self, parent=None):
        super(NIpv6Form, self).__init__(parent)
        self.setPlaceholderText('example: 2001::A:1')
        self.setValidator(NIpv6Validator(self))


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

class NAction(QAction):
    def __init__(self, text, parent=None):
        super(NAction, self).__init__(text, parent)
        self.setIconVisibleInMenu(True)
