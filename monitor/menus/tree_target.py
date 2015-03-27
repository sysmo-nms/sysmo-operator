from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from PyQt5.QtCore import QUrl
from monitor.dialogs.user_operations import UserOperationsWizard
from monitor.dialogs.new_probe import NewProbe
from monitor.dialogs.properties.target import openPropertiesFor
from sysmo_widgets import NAction
from functools import partial
import monitor.api as monapi
import supercast.main as supercast
import sysmapi


class TargetMenu(QMenu):
    def __init__(self, parent):
        super(TargetMenu, self).__init__(parent)
        self._tuOperationWiz  = None
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localMenu    = QMenu(self.tr('Local operations'), self)
        self.localMenu.setIcon(QIcon(sysmapi.nGetPixmap('utilities-terminal')))

        self.configureAction = NAction(self.tr('Configure new action'), self)
        self.configureAction.setPriority(QAction.HighPriority)
        self.addMenu(self.localMenu)
        self.addAction(self.configureAction)
        #######################################################################

        self.addSeparator()

        action = NAction(self.tr('Add a new probe'), self)
        action.triggered.connect(self._newProbe)
        action.setIcon(QIcon(sysmapi.nGetPixmap('list-add')))
        self.addAction(action)

        action = NAction(self.tr('Locate on map'), self)
        action.triggered.connect(self._locateOnMap)
        self.addAction(action)

        action = NAction(self.tr('Delete this target...'), self)
        action.triggered.connect(self._deleteTarget)
        action.setIcon(QIcon(sysmapi.nGetPixmap('process-stop')))
        self.addAction(action)

        self.addSeparator()

        action = NAction(self.tr('Performances Dashboard...'), self)
        action.triggered.connect(self._openDocEngine)
        action.setIcon(QIcon(sysmapi.nGetPixmap('utilities-system-monitor')))
        self.addAction(action)

        action = NAction(self.tr('Documentation...'), self)
        action.triggered.connect(self._openDocEngine)
        action.setIcon(QIcon(sysmapi.nGetPixmap('folder-saved-search')))
        self.addAction(action)

        self.addSeparator()

        action = NAction(self.tr('Properties...'), self)
        action.triggered.connect(self._openProperties)
        action.setIcon(QIcon(sysmapi.nGetPixmap('edit-paste')))
        self.addAction(action)

        self.addSeparator()


    def _openPerfDash(self): pass
    
    def showMenuFor(self, target, point):
        uactions = monapi.getUOperationsFor(target)
        self._currentTarget = target
        if self._tuOperationWiz != None:
            self.configureAction.triggered.disconnect(self._tuOperationWiz)
        self._tuOperationWiz = partial(self._launchUserOperationsWiz, target)
        self.configureAction.triggered.connect(self._tuOperationWiz)
        if len(uactions) == 0:
            self.localMenu.setDisabled(True)
        else:
            self.localMenu.setDisabled(False)
            self.localMenu.clear()
            bold = True
            bfont = QFont()
            bfont.setUnderline(True)
            for i in range(len(uactions)):
                qa = NAction(uactions[i], self)
                if bold == True:
                    qa.setFont(bfont)
                    bold = False
                callback = partial(self._userOperation, target, uactions[i])
                qa.triggered.connect(callback)
                self.localMenu.addAction(qa)

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    #######
    # API #
    #######
    def _launchUserOperationsWiz(self, elem):
        uaWiz = UserOperationsWizard(self, element=elem)

    def _createProbeOperation(self, msg):
        print(("create prboe ", msg))

    def _userOperation(self, element, action):
        monapi.execUOperation(action, element)

    def _openDocEngine(self):
        # WTF TODO docengine not used?
        url = QUrl('http://www.wikipedia.org/wiki/%s' % self._currentTarget)
        QDesktopServices.openUrl(url)

    def _deleteTarget(self):
        msgBox = QMessageBox()
        msgBox.setText('You are about to delete a target.')
        msgBox.setInformativeText('Do you want to continue?')
        msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        msgBox.setIcon(QMessageBox.Warning)
        r = msgBox.exec_()
        if r == QMessageBox.Apply:
            pdu = {
                'from': 'monitor',
                'type': 'deleteTargetQuery',
                'value': {
                    'name': self._currentTarget
                }
            }
            supercast.send(pdu, self._deleteTargetReply)
    
    def _deleteTargetReply(self, msg):
        print(("reply, ", msg))

    def _newProbe(self):
        cpWiz = NewProbe(self._currentTarget)
        cpWiz.show()

    def _openProperties(self):
        openPropertiesFor(self._currentTarget)
        print(("properties: ", self._currentTarget))

    def _locateOnMap(self):
        print(("locate on map: ", self._currentTarget))
