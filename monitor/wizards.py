from    PyQt5.QtCore       import *
from    PyQt5.QtGui        import *
import  sysmapi

class AddTargetWizard(QWizard):
    def __init__(self, parent=None):
        super(AddTargetWizard, self).__init__(parent)
        self.setModal(False)
        self.setWindowTitle(self.tr('Create a target'))
        self.setPixmap(QWizard.WatermarkPixmap, sysmapi.nGetIcon('list-add').pixmap(100,100))
        #self.setPixmap(QWizard.LogoPixmap, TkorderIcons.get('list-add').pixmap(100,100))
        self.setPixmap(QWizard.BannerPixmap, sysmapi.nGetIcon('list-add').pixmap(100,100))
        self.setPixmap(QWizard.BackgroundPixmap, sysmapi.nGetIcon('list-add').pixmap(100,100))
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        self.setOption(QWizard.NoBackButtonOnStartPage)
        self.addPage(self.stepOne())
        self.addPage(self.stepTwo())
        self.addPage(self.stepThree())
        self.show()

    def stepOne(self):
        page = QWizardPage(self)
        page.setTitle(self.tr('Create a new target'))
        page.setSubTitle('blabla')
        label = QLabel(self.tr('This wizard will help you to create a new target'))
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def stepTwo(self):
        page = QWizardPage(self)
        page.setTitle(self.tr('step 2'))
        label = QLabel(self.tr('bla bal bal'))
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def stepThree(self):
        page = QWizardPage(self)
        page.setFinalPage(True)
        page.setTitle(self.tr('step 3'))
        label = QLabel(self.tr('bla bal bal'))
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

class AddTargetForm(QDialog):
    def __init__(self, parent=None):
        super(AddTargetForm, self).__init__(parent)

class AddProbeForm(QDialog):
    def __init__(self, parent=None):
        super(AddProbeForm, self).__init__(parent)
