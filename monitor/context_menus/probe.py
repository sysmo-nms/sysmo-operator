from    PyQt5.QtGui        import QIcon
from    PyQt5.QtWidgets    import (
    QMenu,
    QAction,
    QErrorMessage,
    QMessageBox

)


from    functools import partial
from    monitor.commands.wizards           import UserActionsWizard
from    monitor.elements_properties.probe.main   import openPropertiesFor
import  monitor.api    as monapi
import  sysmapi
import  supercast.main as supercast

class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._puActionWiz   = None
        self._showPerfs     = None
        self.setIcon(QIcon(sysmapi.nGetPixmap('folder-saved-search')))

        self._infoBox = QErrorMessage(self)
        self._infoBox.setModal(True)

        action = QAction(self.tr('Force check'), self)
        action.triggered.connect(self._forceCheck)
        action.setIcon(QIcon(sysmapi.nGetPixmap('software-update-available')))
        self.addAction(action)

        action = QAction(self.tr('Suspend probe'), self)
        action.triggered.connect(self._suspendProbe)
        #action.setIcon(sysmapi.nGetIcon('media-playback-pause'))
        self.addAction(action)


        action = QAction(self.tr('Delete this probe'), self)
        action.triggered.connect(self._deleteProbe)
        action.setIcon(QIcon(sysmapi.nGetPixmap('process-stop')))
        self.addAction(action)

        self.addSeparator()

        self._performances = QAction(self.tr('Performances...'), self)
        self._performances.triggered.connect(self._openProperties)
        self._performances.setIcon(QIcon(sysmapi.nGetPixmap('utilities-system-monitor')))
        self.addAction(self._performances)

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
        trayicon = sysmapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Suspend check succeeded blablabla bla...', msecs=3000)
        print(("suspend probe ", self._currentProbe))

    def _forceCheck(self):
        supercast.send(
            'monitorForceProbeQuery',
            (self._currentProbe),
            self._forceProbeReply
        )

    def _forceProbeReply(self, msg):
        trayicon = sysmapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Force check succeeded...', msecs=3000)

    def _locateOnMap(self):
        print(("locate on map: ", self._currentProbe))

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
        print(("delete probe: ", msg))

    def _openProperties(self):
        openPropertiesFor(self._currentProbe, 'performances')
