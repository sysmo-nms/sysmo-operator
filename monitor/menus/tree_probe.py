from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction, QErrorMessage, QMessageBox
from monitor.windows.performances import openPerformancesFor

import supercast.main as supercast
import sysmapi

class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._showPerfs     = None
        self.setIcon(QIcon(sysmapi.nGetPixmap('folder-saved-search')))

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
        self._performances.triggered.connect(self._openPerformances)
        self._performances.setIcon(QIcon(sysmapi.nGetPixmap('utilities-system-monitor')))
        self.addAction(self._performances)

    def showMenuFor(self, probe, point):
        self._currentProbe = probe
        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    #######
    # API #
    #######
    def _suspendProbe(self):
        trayicon = sysmapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Suspend check succeeded blablabla bla...', msecs=3000)
        print(("suspend probe ", self._currentProbe))

    def _forceCheck(self):
        pdu = {
            'from': 'monitor',
            'type': 'forceProbeQuery',
            'value': {
                'name': self._currentProbe
            }
        }
        supercast.send(pdu, self._forceProbeReply)

    def _forceProbeReply(self, msg):
        trayicon = sysmapi.nGetSystemTrayIcon()
        trayicon.showMessage('Command return:', 'Force check succeeded...', msecs=3000)

    def _locateOnMap(self):
        print(("locate on map: ", self._currentProbe))

    def _deleteProbe(self):
        msgBox = QMessageBox()
        msgBox.setText('You are about to delete a probe.')
        msgBox.setInformativeText('Do you want to continue?')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setIcon(QMessageBox.Warning)
        r = msgBox.exec_()
        if r == QMessageBox.Yes:
            pdu = {
                'from': 'monitor',
                'type': 'deleteProbeQuery',
                'value': {
                    'name': self._currentProbe
                }
            }
            supercast.send(pdu, self._deleteProbeReply)

    def _deleteProbeReply(self, msg):
        print(("delete probe: ", msg))

    def _openPerformances(self):
        openPerformancesFor(self._currentProbe, 'performances')
