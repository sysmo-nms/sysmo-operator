from    PySide.QtGui    import (
    QFrame,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QPixmap,
    QTransform

)
from    PySide.QtCore   import QUrl, Qt
from    PySide.QtSvg    import QSvgWidget
import  noctopus

class Central(QFrame):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        grid = self.initLocator()
        self.setLayout(grid)

    def initLocator(self):
        ad = Add(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"

class Add(QFrame):
    def __init__(self, parent):
        super(Add, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        grid            = QGridLayout(self)
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
        centralFrame    = QFrame(self)
        centralGrid     = QGridLayout(centralFrame)

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
        separator = QFrame(self)
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
        scFrame = QFrame(self)
        scGrid  = QGridLayout(scFrame)
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
        insertFrame = QFrame(self)
        insertGrid = QGridLayout(insertFrame)
        insertGrid.addWidget(QLabel('Insert license key:', self),   0,0)
        insertGrid.addWidget(QLineEdit(self),                       0,1)
        insertGrid.addWidget(QPushButton('Activate', self),         0,2)
        insertFrame.setLayout(insertGrid)
        return insertFrame

    def generateFormatedText(self):
        text = '''
            <h1>The Locator Opus</h1>
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            <p>qsdfqsdfffffff qsdf qsdf qsdfqsdflkjqsdlfkj qsdlkj qsdflkj qdslfkj 
            A PySide.QtGui.QTextDocument can be edited programmatically using a PySide.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PySide.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PySide.QtGui.QTextDocument.begin() , PySide.QtGui.QTextDocument.end() , and PySide.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
            </p>
            <h2>Fonctionnality</h2>
            <p>
            A PySide.QtGui.QTextDocument can be edited programmatically using a PySide.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PySide.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PySide.QtGui.QTextDocument.begin() , PySide.QtGui.QTextDocument.end() , and PySide.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
            </p>
            <h2>Benefits</h2>
            <p>
            A PySide.QtGui.QTextDocument can be edited programmatically using a PySide.QtGui.QTextCursor , and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the PySide.QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use PySide.QtGui.QTextDocument.begin() , PySide.QtGui.QTextDocument.end() , and PySide.QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.
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
    
class Banner60(QFrame):
    def __init__(self, parent):
        super(Banner60, self).__init__(parent)
        grid = QGridLayout(self)
        banner = QSvgWidget(noctopus.getImage('60-day-trial-banner'), self)
        banner.setFixedHeight(300)
        banner.setFixedWidth(300)
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        grid.addWidget(banner, 0,0)
