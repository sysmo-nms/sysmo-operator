from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPalette, QColor, QImage
from PyQt5.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionProgressBar, QApplication
import monitor.gui.tree.tree_model as treemod
import sysmapi

class StatusItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(StatusItemDelegate, self).__init__(parent)

        self._imageSize = QSize(25,25)

    def paint(self, painter, option, index):
#         status    = index.data(Qt.DisplayRole)
#         cartouche = QRect(option.rect)
#         if option.state & QStyle.State_Selected:
#             painter.fillRect(option.rect, option.palette.highlight())
#         if status == 'nodata':
#             painter.drawText(cartouche, Qt.AlignCenter, '')
#             return
#             
#         cartouche.setSize(self._imageSize)
#         if status == 'DOWN':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('weather-severe-alert')))
#         elif status == 'OK':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('weather-clear')))
#         elif status == 'WARNING':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('weather-showers')))
#         elif status == 'CRITICAL':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('weather-severe')))

            #QStyledItemDelegate.paint(self, painter, option, index)
            #return


        #painter.drawImage(cartouche, self._okImage)
        QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        return self._imageSize

class ProgressItemDelegate2(QStyledItemDelegate):
    def __init__(self, parent):
        super(ProgressItemDelegate2, self).__init__(parent)
    def paint(self,painter,option,index):
        QStyledItemDelegate.paint(self, painter, option, index)

class ProgressItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ProgressItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self,painter,option,index)
        painter.save()

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
        painter.restore()


class TriggerItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(TriggerItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "paint from trigger delegate!"
        QStyledItemDelegate.paint(self, painter, option, index)

class StateItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(StateItemDelegate, self).__init__(parent)

        self._imageSize = QSize(25,25)

    def paint(self, painter, option, index):
        state    = index.data(Qt.DisplayRole)
        cartouche = QRect(option.rect)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        if state == 'nodata':
            painter.drawText(cartouche, Qt.AlignCenter, '')
            return
#             
#         cartouche.setSize(self._imageSize)
#         if state == 'running':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('media-playback-start')))
#         elif state == 'paused':
#             painter.drawImage(cartouche, QImage(sysmapi.nGetImage('media-playback-pause')))
        QStyledItemDelegate.paint(self, painter, option, index)

        
    def sizeHint(self, option, index):
        return self._imageSize

class HostItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(HostItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
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
