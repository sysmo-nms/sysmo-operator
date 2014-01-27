from    PySide.QtCore       import *
from    PySide.QtGui        import *
import  TkorderIcons
class AddTargetWizard(QWizard):
    def __init__(self, parent=None):
        super(AddTargetWizard, self).__init__(parent)
        self.setModal(False)
        self.setWindowTitle('Create a target')
        self.setPixmap(QWizard.WatermarkPixmap, TkorderIcons.get('list-add').pixmap(100,100))
        #self.setPixmap(QWizard.LogoPixmap, TkorderIcons.get('list-add').pixmap(100,100))
        self.setPixmap(QWizard.BannerPixmap, TkorderIcons.get('list-add').pixmap(100,100))
        self.setPixmap(QWizard.BackgroundPixmap, TkorderIcons.get('list-add').pixmap(100,100))
        self.setOption(QWizard.ExtendedWatermarkPixmap)
        self.setOption(QWizard.NoBackButtonOnStartPage)
        self.addPage(self.stepOne())
        self.addPage(self.stepTwo())
        self.addPage(self.stepThree())
        self.show()

    def stepOne(self):
        page = QWizardPage(self)
        page.setTitle('Create a new target')
        page.setSubTitle('blabla')
        label = QLabel('This wizard will help you to create a new target')
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def stepTwo(self):
        page = QWizardPage(self)
        page.setTitle('step 2')
        label = QLabel('bla bal bal')
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def stepThree(self):
        page = QWizardPage(self)
        page.setFinalPage(True)
        page.setTitle('step 3')
        label = QLabel('bla bal bal')
        label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        page.setLayout(layout)
        return page
