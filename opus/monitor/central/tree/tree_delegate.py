from    PySide.QtCore   import (
    Qt,
    QSize
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
            option.rect.setSize(self._rrdToolSize)
            if option.state == QStyle.State_Selected:
                painter.setBrush(option.palette.hightlightedText())
                painter.setPen(Qt.Red)
            painter.drawImage(option.rect, self._rrdToolLogo)
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


class StatusItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(StatusItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from status delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

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


class MonitorItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(MonitorItemDelegate, self).__init__(parent)
        self._rrdToolLogo   = QImage(nocapi.nGetImage('rrdtool-logo'))
        self._rrdToolSize   = QSize(80,25)

    def paint(self, painter, option, index):

        print "paint: ", index.data(Qt.UserRole + 1), " ", index.column()
        if index.data(Qt.UserRole + 1) == None:
            # it is a column child
            # get the root item
            itemRoot = index.sibling(index.row(), 0)
            print "paint itemroot"
            if itemRoot.data(Qt.UserRole + 1) == "Probe":
                # is is a probe check for columns
                if index.column() == 1:
                    if itemRoot.data(Qt.UserRole + 2) == True:
                        option.rect.setSize(self._rrdToolSize)
                        painter.drawImage(option.rect, self._rrdToolLogo)
                    else:
                        return
                elif index.column() == 2:
                    testouille = itemRoot.data(Qt.DisplayRole)
                    print "paint (from dataChanged?): ", testouille
                    timeout     = itemRoot.data(Qt.UserRole + 6)
                    step        = itemRoot.data(Qt.UserRole + 5)
                    progress    = itemRoot.data(Qt.UserRole + 4)

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
                elif index.column() == 4:
                    timeout     = itemRoot.data(Qt.UserRole + 6)
                    step        = itemRoot.data(Qt.UserRole + 5)
                    painter.drawText(option.rect, Qt.AlignVCenter, '%s/%s' % (step,timeout))
                elif index.column() == 5:
                    state       = itemRoot.data(Qt.UserRole + 7)
                    if state == 1:
                        s = 'running'
                    else:
                        s = 'suspended'
                    painter.drawText(option.rect, Qt.AlignCenter, '%s' % (s))
                elif index.column() == 7:
                    pconf       = itemRoot.data(Qt.UserRole + 8)
                    painter.drawText(option.rect, Qt.AlignVCenter|Qt.AlignLeft, '%s' % (pconf))
                else:
                    return
            elif itemRoot.data(Qt.UserRole + 1) == "Target":
                if index.column() == 6:
                    ip       = itemRoot.data(Qt.UserRole + 2)
                    painter.drawText(option.rect, Qt.AlignCenter, '%s' % ip)
                else:
                    return
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

class PBarRedPalette(QPalette):
    def __init__(self):
        super(PBarRedPalette, self).__init__()
        red = QColor(204,0,0)
        self.setColor(QPalette.Highlight, red)
