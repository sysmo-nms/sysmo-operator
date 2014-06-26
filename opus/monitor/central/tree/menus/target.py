from    PySide.QtGui    import (
    QMenu,
    QFont,
    QAction
)

from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
from    opus.monitor.central.tree.logwin        import LoggerView
from    noctopus_widgets                        import NAction
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

        self.configureAction = NAction(self.tr('Configure new action'), self)
        self.configureAction.setPriority(QAction.HighPriority)
        self.addMenu(self.localMenu)
        self.addAction(self.configureAction)
        #######################################################################

        self.addSeparator()

        action = NAction(self.tr('Locate on map'), self)
        self.addAction(action)

        action = NAction(self.tr('Delete this target ans his probes'), self)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()

        action = NAction(self.tr('Documentation'), self)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        self.addSeparator()

        action = NAction(self.tr('Properties'), self)
        action.setIcon(nocapi.nGetIcon('edit-paste'))
        self.addAction(action)

        self.addSeparator()






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

    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _createProbeAction(self, msg):
        print "create prboe ", msg

    def _userAction(self, element, action):
        monapi.execUAction(action, element)


