from    PySide.QtGui    import (
    QMenu,
    QAction
)

from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
from    opus.monitor.logwin.main                import openLoggerFor
from    opus.monitor.central.tree.toolbox       import openProbePropertiesFor
import  opus.monitor.api    as monapi
import  nocapi

class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._puActionWiz   = None
        self._showPerfs     = None
        self.setIcon(nocapi.nGetIcon('folder-saved-search'))
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localProbeMenu    = QMenu(self.tr('Local Actions'), self)
        self.localProbeMenu.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self.localProbeMenu.setDisabled(True)

        self.configureProbeAction = QAction(self.tr('Configure actions'), self)
        self.addMenu(self.localProbeMenu)
        self.addAction(self.configureProbeAction)
        #######################################################################

        self.addSeparator()

        action = QAction(self.tr('Force check'), self)
        action.triggered.connect(self._forceCheck)
        action.setIcon(nocapi.nGetIcon('software-update-available'))
        self.addAction(action)

        action = QAction(self.tr('Suspend probe'), self)
        action.triggered.connect(self._suspendProbe)
        #action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Locate on map'), self)
        action.triggered.connect(self._locateOnMap)
        #action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Delete this probe'), self)
        action.triggered.connect(self._deleteProbe)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Documentation'), self)
        action.triggered.connect(self._openDocumentation)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        self.addSeparator()

        self._performances = QAction(self.tr('Performances'), self)
        self._performances.triggered.connect(self._openPerformances)
        self._performances.setIcon(nocapi.nGetIcon('utilities-system-monitor'))
        self.addAction(self._performances)

        self.addSeparator()

        action = QAction(self.tr('Properties'), self)
        action.triggered.connect(self._openProperties)
        action.setIcon(nocapi.nGetIcon('edit-paste'))
        self.addAction(action)

    def showMenuFor(self, probe, point):
        self._currentProbe = probe
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

    #######
    # API #
    #######
    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _userAction(self, element, action):
        monapi.execUAction(action, element)

    def _suspendProbe(self):
        print "suspend probe ", self._currentProbe

    def _forceCheck(self):
        print "force check ", self._currentProbe

    def _locateOnMap(self):
        print "locate on map: ", self._currentProbe

    def _deleteProbe(self):
        print "delete probe ", self._currentProbe

    def _openProperties(self):
        openProbePropertiesFor(self._currentProbe)

    def _openPerformances(self):
        openLoggerFor(self._currentProbe, 'performances')

    def _openDocumentation(self):
        print "open documentation: ", self._currentProbe
