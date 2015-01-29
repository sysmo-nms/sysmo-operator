from    PyQt4.QtGui    import (
    QFrame,
    QPushButton,
    QLineEdit,
    QLabel,
    QPixmap,
    QTransform,
    QMenu

)
from noctopus_widgets   import (
    NGridContainer,
    NFrameContainer,
    NGrid,
    NFrame
)
from    PyQt4.QtCore   import QUrl, Qt
from    PyQt4.QtSvg    import QSvgWidget
import    nocapi

class Central(NFrameContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        grid = self.initLocator()
        self.setLayout(grid)
        menu = QMenu('netman', self)
        menu.setIcon(nocapi.nGetIcon('network-wired'))
        nocapi.nAddMainMenu(menu)

    def initLocator(self):
        ad = Add(self)
        grid = NGridContainer(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print("toggle")

class Add(NFrame):
    def __init__(self, parent):
        super(Add, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        grid            = NGrid(self)
        centralWidget   = self.generateCentralWidget()
        banner          = Banner60(self)
        banner.move(-15,-15)
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

        moreInfoButton      = QPushButton('About Locator',  self)
        moreInfoButton.clicked.connect(self.showLocatorDescr)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)
        startTrialButton    = QPushButton('Start Trial',    self)
        printQuote          = QPushButton('Print quote',     self)
        screenShots         = QPushButton('Screenshots',     self)

        centralGrid.addWidget(startTrialButton, 0,0)
        centralGrid.addWidget(getLicenceButton, 1,0)
        centralGrid.addWidget(printQuote,       2,0)
        centralGrid.addWidget(moreInfoButton,   3,0)
        centralGrid.addWidget(screenShots,      4,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,6,2)

        # separator
        separator = NFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Raised)
        centralGrid.addWidget(separator,            6,0,1,3)

        # insert key
        insertKeyLabel = QLabel('Insert license key: ', self)
        insertKeyLineEdit = QLineEdit(self)
        insertKeyButton   = QPushButton('Activate', self)

        centralGrid.addWidget(insertKeyLabel,       7,0)
        centralGrid.addWidget(insertKeyLineEdit,    7,1)
        centralGrid.addWidget(insertKeyButton,      7,2)

        # screenshot
        apix = QPixmap('./commercials/snapshot_tko4.png')
        bpix = apix.scaledToHeight(200, Qt.SmoothTransformation)
        cpix = bpix.transformed(QTransform().rotate(3))
        scFrame = NFrame(self)
        scGrid  = NGrid(scFrame)
        scLabel1 = QLabel(self)
        scLabel1.setPixmap(cpix)
        scGrid.addWidget(scLabel1,  0,0)
        scGrid.setRowStretch(0,0)
        scGrid.setRowStretch(2,1)
        scFrame.setLayout(scGrid)

        centralGrid.addWidget(scFrame, 0,3,8,1)
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
        text = '''
            <h1>The Netman Opus</h1>
            <h2>The locator</h2>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            <h2>The ipHelper</h2>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            <h2>The arpwatcher</h2>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            <h2>The trap handler</h2>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            <h2>The wifiman</h2>
            <p>802.1x, traffic </p>
            <h2>The ipcalc utils</h2>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            A PyQt4.QtGui.QTextDocument can be edited programmatically using a PyQt4.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PyQt4.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PyQt4.QtGui.QTextDocument.begin() , PyQt4.QtGui.QTextDocument.end() , and PyQt4.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
            </p>
            <h2>Fonctionnality</h2>
            <p>
            A PyQt4.QtGui.QTextDocument can be edited programmatically using a PyQt4.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PyQt4.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PyQt4.QtGui.QTextDocument.begin() , PyQt4.QtGui.QTextDocument.end() , and PyQt4.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
            </p>
            <h2>Benefits</h2>
            <p>
            A PyQt4.QtGui.QTextDocument can be edited programmatically using a PyQt4.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PyQt4.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PyQt4.QtGui.QTextDocument.begin() , PyQt4.QtGui.QTextDocument.end() , and PyQt4.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
            </p>
        '''
        #document = QTextDocument(self)
        #document.setHtml(text)
        #roEdit  = QTextEdit(self)
        #roEdit.setDocument(document)
        label = QLabel(text,self)
        label.setWordWrap(True)
        return label

    def showLocatorDescr(self):
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
