from    PyQt5.QtGui    import (
    QDesktopServices,
    QFont,
    QIcon
)
from    PyQt5.QtWidgets    import (
    QMenu,
    QAction,
    QMessageBox
)
from PyQt5.QtCore import QUrl

from    functools import partial
from    monitor.commands.wizards           import UserActionsWizard
from    monitor.gui.tree.add_probe             import AddProbe
from    monitor.elements_properties.target import openPropertiesFor
from    sysmo_widgets                        import NAction
import  monitor.api                        as monapi
import  sysmapi
import  supercast.main as supercast


class TargetMenu(QMenu):
    def __init__(self, parent):
        super(TargetMenu, self).__init__(parent)
        self._tuActionWiz  = None
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localMenu    = QMenu(self.tr('Local Actions'), self)
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


    def showMenuFor(self, target, point):
        uactions = monapi.getUActionsFor(target)
        self._currentTarget = target
        if self._tuActionWiz != None:
            self.configureAction.triggered.disconnect(self._tuActionWiz)
        self._tuActionWiz = partial(self._launchUserActionsWiz, target)
        self.configureAction.triggered.connect(self._tuActionWiz)
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
                callback = partial(self._userAction, target, uactions[i])
                qa.triggered.connect(callback)
                self.localMenu.addAction(qa)

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    #######
    # API #
    #######
    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _createProbeAction(self, msg):
        print(("create prboe ", msg))

    def _userAction(self, element, action):
        monapi.execUAction(action, element)

    def _openDocEngine(self):
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
            supercast.send(
                'monitorDeleteTargetQuery',
                (self._currentTarget),
                self._deleteTargetReply
            )
    
    def _deleteTargetReply(self, msg):
        print(("reply, ", msg))

    def _newProbe(self):
        cpWiz = AddProbe(self._currentTarget, self)

    def _openProperties(self):
        openPropertiesFor(self._currentTarget)
        print(("properties: ", self._currentTarget))

    def _locateOnMap(self):
        print(("locate on map: ", self._currentTarget))
