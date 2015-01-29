from    PyQt5.QtGui    import (
    QFrame,
    QPushButton,
    QLabel,
    QLineEdit,
    QMenu
)
from    noctopus_widgets    import (
    NFrame,
    NFrameContainer,
    NGrid,
    NGridContainer
)

from    PyQt5.QtCore   import QUrl
from    PyQt5.QtWebKit import QWebView
from    PyQt5.QtSvg    import QSvgWidget
import    nocapi

class Central(NFrameContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        self.enabled = True
        menu = QMenu('knowledge', self)
        menu.setIcon(nocapi.nGetIcon('accessories-text-editor'))
        nocapi.nAddMainMenu(menu)
        grid = self._initKnowledgeLayout()
        self.setLayout(grid)

    def _initKnowledgeLayout(self):
        if self.enabled == False:
            widget  = Add(self)
        elif self.enabled == True:
            widget  = App(self)
        grid    = NGridContainer(self)
        grid.addWidget(widget, 0,0)
        return grid

    def toggleButtonClicked(self):
        print("toggle")

class App(NFrame):
    def __init__(self, parent):
        super(App, self).__init__(parent)
        grid = NGrid(self)
        self.setContentsMargins(0,0,0,0)
        grid.setContentsMargins(0,0,0,0)

        server  = 'localhost'
        wiki = QWebView(self)
        wiki.load(QUrl("http://%s:8080/wiki_base.html" % server))

        controls = self.initControls()

        grid.addWidget(controls,    0,0)
        grid.addWidget(wiki,        1,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        self.setLayout(grid)

    def initControls(self):
        cFrame = NFrameContainer(self)
        cGrid = NGrid(cFrame)

        forceButton = QPushButton(
            nocapi.nGetIcon('dialog-warning'),
            'Force auto edit', cFrame)
        cGrid.addWidget(forceButton,    0,0)
        cGrid.setColumnStretch(0,0)
        cGrid.setColumnStretch(1,1)

        cFrame.setLayout(cGrid)
        return cFrame

class Add(NFrame):
    def __init__(self, parent):
        super(Add, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        grid            = NGrid(self)
        centralWidget   = self.generateCentralWidget()
        banner          = Banner60(self)
        banner.move(-15,-15)
        #grid.addWidget(banner, 0,0)
        grid.addWidget(centralWidget, 1,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,1)

        self.setLayout(grid)

    def generateCentralWidget(self):
        centralFrame    = NFrame(self)
        centralGrid     = NGrid(centralFrame)

        moreInfoButton      = QPushButton('About Knowledge',  self)
        moreInfoButton.clicked.connect(self.showKnowledgeDescr)
        startTrialButton    = QPushButton('Start Trial',    self)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)
        printQuote          = QPushButton('Print quote',     self)

        centralGrid.addWidget(getLicenceButton, 0,0)
        centralGrid.addWidget(startTrialButton, 1,0)
        centralGrid.addWidget(printQuote,       2,0)
        centralGrid.addWidget(moreInfoButton,   3,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,4,1)

        insertKey = self.generateInsertKeyForm()
        centralGrid.addWidget(insertKey,         4,0,1,2)
        centralFrame.setLayout(centralGrid)

        return centralFrame

    def generateInsertKeyForm(self):
        insertFrame = NFrame(self)
        insertGrid = NGrid(insertFrame)
        insertGrid.addWidget(QLabel('Insert license key:', self),   0,0)
        insertGrid.addWidget(QLineEdit(self),                       0,1)
        insertGrid.addWidget(QPushButton('Activate', self),         0,2)
        insertFrame.setLayout(insertGrid)
        return insertFrame

    def generateFormatedText(self):
        return QLabel('Knowledge tool descriptions et screenshots', self)

    def showKnowledgeDescr(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

    def showUpdateLicence(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

class Banner60(NFrame):
    def __init__(self, parent):
        super(Banner60, self).__init__(parent)
        grid = NGrid(self)
        banner = QSvgWidget(nocapi.nGetImage('60-day-trial-banner'), self)
        banner.setFixedHeight(300)
        banner.setFixedWidth(300)
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        grid.addWidget(banner, 0,0)
