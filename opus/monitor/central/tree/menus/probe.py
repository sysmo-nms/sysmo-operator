from    PySide.QtGui    import (
    QMenu,
    QAction,
    QErrorMessage,
    QMessageBox

)


from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
from    opus.monitor.logwin.main                import openLoggerFor
from    opus.monitor.central.tree.toolbox       import openProbePropertiesFor
import  opus.monitor.api    as monapi
import  nocapi
import  supercast.main as supercast

class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._puActionWiz   = None
        self._showPerfs     = None
        self.setIcon(nocapi.nGetIcon('folder-saved-search'))

        self._infoBox = QErrorMessage(self)
        self._infoBox.setModal(True)

        action = QAction(self.tr('Force check'), self)
        action.triggered.connect(self._forceCheck)
        action.setIcon(nocapi.nGetIcon('software-update-available'))
        self.addAction(action)

        action = QAction(self.tr('Suspend probe'), self)
        action.triggered.connect(self._suspendProbe)
        #action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)


        action = QAction(self.tr('Delete this probe'), self)
        action.triggered.connect(self._deleteProbe)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()

        self._performances = QAction(self.tr('Performances...'), self)
        self._performances.triggered.connect(self._openPerformances)
        self._performances.setIcon(nocapi.nGetIcon('utilities-system-monitor'))
        self.addAction(self._performances)

        self.addSeparator()

        action = QAction(self.tr('Properties...'), self)
        action.triggered.connect(self._openProperties)
        action.setIcon(nocapi.nGetIcon('edit-paste'))
        self.addAction(action)

    def showMenuFor(self, probe, point):
        self._currentProbe = probe
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
        #print "result is: ", self._infoBox.result()
        trayicon = nocapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Suspend check succeeded blablabla bla...', msecs=3000)
        print "suspend probe ", self._currentProbe

    def _forceCheck(self):
        #self._infoBox.showMessage("You are about to edforce a probe check. Is it allright?", "alert_force_check")
        #self._infoBox.exec_()
        supercast.send(
            'monitorForceProbeQuery',
            (self._currentProbe),
            self._forceProbeReply
        )

    def _forceProbeReply(self, msg):
        trayicon = nocapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Force check succeeded...', msecs=3000)

    def _locateOnMap(self):
        print "locate on map: ", self._currentProbe

    def _deleteProbe(self):
        msgBox = QMessageBox()
        msgBox.setText('You are about to delete a probe.')
        msgBox.setInformativeText('Do you want to continue?')
        msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        msgBox.setIcon(QMessageBox.Warning)
        r = msgBox.exec_()
        if r == QMessageBox.Apply:
            supercast.send(
                'monitorDeleteProbeQuery',
                (self._currentProbe),
                self._deleteProbeReply
            )

    def _deleteProbeReply(self, msg):
        print "delete probe: ", msg

    def _openProperties(self):
        openProbePropertiesFor(self._currentProbe)

    def _openPerformances(self):
        openLoggerFor(self._currentProbe, 'performances')
