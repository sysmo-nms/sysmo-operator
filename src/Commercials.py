from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
import  TkorderIcons

class LocatorAd(QFrame):
    def __init__(self, parent):
        super(LocatorAd, self).__init__(parent)
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
        startTrialButton    = QPushButton('Start Trial',    self)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)

        centralGrid.addWidget(getLicenceButton, 0,0)
        centralGrid.addWidget(startTrialButton, 1,0)
        centralGrid.addWidget(moreInfoButton,   2,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,4,1)

        insertKey = self.generateInsertKeyForm()
        centralGrid.addWidget(insertKey,         4,0,1,2)
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
        return QLabel('locator descriptions et screenshots', self)

    def showLocatorDescr(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

    def showUpdateLicence(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)
    


class LogAd(QFrame):
    def __init__(self, parent):
        super(LogAd, self).__init__(parent)
        grid            = QGridLayout(self)
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
        centralFrame    = QFrame(self)
        centralGrid     = QGridLayout(centralFrame)

        moreInfoButton      = QPushButton('About Log',  self)
        moreInfoButton.clicked.connect(self.showLogDescr)
        startTrialButton    = QPushButton('Start Trial',    self)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)

        centralGrid.addWidget(getLicenceButton, 0,0)
        centralGrid.addWidget(startTrialButton, 1,0)
        centralGrid.addWidget(moreInfoButton,   2,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,4,1)

        insertKey = self.generateInsertKeyForm()
        centralGrid.addWidget(insertKey,         4,0,1,2)
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
        return QLabel('Log viewer descriptions et screenshots', self)

    def showLogDescr(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

    def showUpdateLicence(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

class BackupAd(QFrame):
    def __init__(self, parent):
        super(BackupAd, self).__init__(parent)
        grid            = QGridLayout(self)
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
        centralFrame    = QFrame(self)
        centralGrid     = QGridLayout(centralFrame)

        moreInfoButton      = QPushButton('About Backup',  self)
        moreInfoButton.clicked.connect(self.showBackupDescr)
        startTrialButton    = QPushButton('Start Trial',    self)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)

        centralGrid.addWidget(getLicenceButton, 0,0)
        centralGrid.addWidget(startTrialButton, 1,0)
        centralGrid.addWidget(moreInfoButton,   2,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,4,1)

        insertKey = self.generateInsertKeyForm()
        centralGrid.addWidget(insertKey,         4,0,1,2)
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
        return QLabel('Backup tool descriptions et screenshots', self)

    def showBackupDescr(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

    def showUpdateLicence(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

class IphelperAd(QFrame):
    def __init__(self, parent):
        super(IphelperAd, self).__init__(parent)
        grid            = QGridLayout(self)
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
        centralFrame    = QFrame(self)
        centralGrid     = QGridLayout(centralFrame)

        moreInfoButton      = QPushButton('About Iphelper',  self)
        moreInfoButton.clicked.connect(self.showIphelperDescr)
        startTrialButton    = QPushButton('Start Trial',    self)
        getLicenceButton    = QPushButton('Get licence key',self)
        getLicenceButton.clicked.connect(self.showUpdateLicence)

        centralGrid.addWidget(getLicenceButton, 0,0)
        centralGrid.addWidget(startTrialButton, 1,0)
        centralGrid.addWidget(moreInfoButton,   2,0)
        
        infoLabel   = self.generateFormatedText()
        centralGrid.addWidget(infoLabel,         0,1,4,1)

        insertKey = self.generateInsertKeyForm()
        centralGrid.addWidget(insertKey,         4,0,1,2)
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
        return QLabel('Iphelper descriptions et screenshots', self)

    def showIphelperDescr(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

    def showUpdateLicence(self):
        url = QUrl('http://www.qtcentre.org/threads/19616-Set-Position-of-QLabel')
        QDesktopServices.openUrl(url)

class Banner60(QFrame):
    def __init__(self, parent):
        super(Banner60, self).__init__(parent)
        grid = QGridLayout(self)
        banner = QSvgWidget(TkorderIcons.getImage('60-day-trial-banner'), self)
        banner.setFixedHeight(300)
        banner.setFixedWidth(300)
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        grid.addWidget(banner, 0,0)

class Banner60Reversed(QFrame):
    def __init__(self, parent):
        super(Banner60Reversed, self).__init__(parent)

class Banner30(QFrame):
    def __init__(self, parent):
        super(Banner30, self).__init__(parent)

class Banner30Reversed(QFrame):
    def __init__(self, parent):
        super(Banner30Reversed, self).__init__(parent)
