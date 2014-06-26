from    PySide.QtGui    import (
    QMenu,
    QAction
)

from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
import  opus.monitor.api    as monapi
import  nocapi

class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._puActionWiz  = None
        self.setIcon(nocapi.nGetIcon('folder-saved-search'))
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localProbeMenu    = QMenu(self.tr('Local Actions'), self)
        self.localProbeMenu.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self.localProbeMenu.setDisabled(True)

        self.configureProbeAction = QAction(self.tr('Configure new action'), self)
        self.addMenu(self.localProbeMenu)
        self.addAction(self.configureProbeAction)
        #######################################################################

        self.addSeparator()

        action = QAction(self.tr('Open log viewew'), self)
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Open probe documentation'), self)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Suspend probe'), self)
        action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Add entry to the probe diary'), self)
        self.addAction(action)

        action = QAction(self.tr('Force check'), self)
        action.setIcon(nocapi.nGetIcon('software-update-available'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Delete this probe'), self)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Properties'), self)
        self.addAction(action)

    def showMenuFor(self, probe, point):
        print "show menu!"
        uactions = monapi.getUActionsFor(probe)
        if self._puActionWiz != None:
            self.configureProbeAction.triggered.disconnect(self._puActionWiz)
        self._puActionWiz = partial(self._launchUserActionsWiz, probe)
        self.configureProbeAction.triggered.connect(self._puActionWiz)
        if len(uactions) == 0:
            self.localProbeMenu.setDisabled(True)
        else:
            self.localProbeMenu.setDisabled(False)
            self.localProbeMenu.clear()
            for i in range(len(uactions)):
                qa = QAction(uactions[i], self)
                callback = partial(self._userAction, probe, uactions[i])
                qa.triggered.connect(callback)
                self.localProbeMenu.addAction(qa)

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _userAction(self, element, action):
        monapi.execUAction(action, element)
