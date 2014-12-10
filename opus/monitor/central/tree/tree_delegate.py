from    PySide.QtCore   import (
    Qt,
    QSize,
    QRect
)

from    PySide.QtGui    import (
    QStyle,
    QStyledItemDelegate,
    QStyleOptionProgressBar,
    QApplication,
    QImage,
    QPalette,
    QColor
)

from    functools import partial
from    opus.monitor.central.tree.tree_model    import ProbeModel
from    opus.monitor.commands.wizards           import UserActionsWizard

import opus.monitor.central.tree.tree_model as treemod

import  opus.monitor.api    as monapi
import  nocapi


class StatusItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(StatusItemDelegate, self).__init__(parent)
        self._okImage = QImage(nocapi.nGetImage('weather-clear'))
        self._okImageSize = QSize(25,25)

    def paint(self, painter, option, index):
        status = index.data(Qt.DisplayRole)
        if status == 'status':
            QStyledItemDelegate.paint(self, painter, option, index)
            return

        cartouche = QRect(option.rect)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        cartouche.setSize(self._okImageSize)

        painter.drawImage(cartouche, self._okImage)
        #QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        return self._okImageSize


class LoggerItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(LoggerItemDelegate, self).__init__(parent)
        self._rrdToolLogo   = QImage(nocapi.nGetImage('rrdtool-logo'))
        self._rrdToolSize   = QSize(80,25)

    def paint(self, painter, option, index):
        loggers = index.data(treemod.LoggerItem.LoggersRole)
        if loggers == None:
            QStyledItemDelegate.paint(self, painter, option, index)
        elif 'bmonitor_logger_rrd2' in loggers:
            cartouche = QRect(option.rect)
            cartouche.setSize(self._rrdToolSize)
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
            painter.drawImage(cartouche, self._rrdToolLogo)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)


class ProgressItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ProgressItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        step    = index.data(treemod.ProgressItem.StepRole)
        if step == None:
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            timeout = index.data(treemod.ProgressItem.TimeoutRole)
            progress  = index.data(treemod.ProgressItem.ProgressRole)
            opts = QStyleOptionProgressBar()
            if progress >= (step + timeout):
                prog = timeout
                prog = timeout - prog
                maxi = timeout
                opts.text    = 'Timeout: %s' % prog
                opts.palette = PBarRedPalette()
            elif progress > step:
                prog = progress - step
                prog = timeout - prog
                maxi = timeout
                opts.text    = 'Timeout: %s' % prog
                opts.palette = PBarRedPalette()
            else:
                prog = progress
                maxi = step
                opts.text    = 'Step: %s' % (step - prog)
    
            opts.rect = option.rect
            opts.textVisible = True
            opts.minimum = 0
            opts.maximum  = maxi
            opts.progress = prog
            QApplication.style().drawControl(QStyle.CE_ProgressBar, opts, painter) 


class TriggerItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(TriggerItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from trigger delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

class StateItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(StateItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from state delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

class HostItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(HostItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from host delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

class TimelineItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(TimelineItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from timeline delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

class PBarRedPalette(QPalette):
    def __init__(self):
        super(PBarRedPalette, self).__init__()
        red = QColor(204,0,0)
        self.setColor(QPalette.Highlight, red)
