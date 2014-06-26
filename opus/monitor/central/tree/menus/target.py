from    PySide.QtGui    import (
    QMenu,
    QAction
)

from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
from    opus.monitor.central.tree.logwin        import LoggerView
import  opus.monitor.api                        as monapi
import  nocapi


class TargetMenu(QMenu):
    def __init__(self, parent):
        super(TargetMenu, self).__init__(parent)
        self._tuActionWiz  = None
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localMenu    = QMenu(self.tr('Local Actions'), self)
        self.localMenu.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self.localMenu.setDisabled(True)

        self.configureAction = QAction(self.tr('Configure new action'), self)
        self.addMenu(self.localMenu)
        self.addAction(self.configureAction)
        #######################################################################

        self.addSeparator()

        action = QAction(self.tr('Suspend all target probes'), self)
        action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Add entry to the target diary'), self)
        self.addAction(action)


        action = QAction(self.tr('Create a new probe'), self)
        action.setIcon(nocapi.nGetIcon('list-add'))
        action.triggered[bool].connect(self._createProbeAction)
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Delete this target ans his probes'), self)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()


        action = QAction(self.tr('Documentation'), self)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        action = QAction(self.tr('History'), self)
        self.addAction(action)

        action = QAction(self.tr('Performances'), self)
        self.addAction(action)

        action = QAction(self.tr('Properties'), self)
        self.addAction(action)

    def showMenuFor(self, target, point):
        uactions = monapi.getUActionsFor(target)
        if self._tuActionWiz != None:
            self.configureAction.triggered.disconnect(self._tuActionWiz)
        self._tuActionWiz = partial(self._launchUserActionsWiz, target)
        self.configureAction.triggered.connect(self._tuActionWiz)
        if len(uactions) == 0:
            self.localMenu.setDisabled(True)
        else:
            self.localMenu.setDisabled(False)
            self.localMenu.clear()
            for i in range(len(uactions)):
                qa = QAction(uactions[i], self)
                callback = partial(self._userAction, target, uactions[i])
                qa.triggered.connect(callback)
                self.localMenu.addAction(qa)

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _createProbeAction(self, msg):
        print "create prboe ", msg

    def _userAction(self, element, action):
        monapi.execUAction(action, element)
