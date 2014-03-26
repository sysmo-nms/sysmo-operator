from    PySide.QtGui        import *
from    PySide.QtCore       import *


class ProbeCriticalButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeCriticalButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('\
        QPushButton {   \
            min-height: 1.5em;              \
            font: bold 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #ef2929,    \
                stop: 1 #cc0000);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #a40000;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #ef2929,    \
                stop: 0 #cc0000);           \
        }')

class ProbeWarningButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeWarningButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('QPushButton {   \
            min-height: 1.5em;              \
            font: bold 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #fcaf3e,    \
                stop: 1 #f57900);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #ce5c00;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #fcaf3e,    \
                stop: 0 #f57900);           \
        }')

class ProbeOkButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeOkButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('QPushButton {   \
            min-height: 1.5em;              \
            font: 1em;                       \
            margin: 0 1px 0 1px;            \
            color: black;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #a1d99b,    \
                stop: 1 #74c476);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #41ab5d;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #a1d99b,    \
                stop: 0 #74c476);           \
        }')

class ProbeUnknownButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeUnknownButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('QPushButton {   \
            min-height: 1.5em;              \
            font: 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #666666,    \
                stop: 1 #222222);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #aaaaaa;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #a1d99b,    \
                stop: 0 #74c476);           \
        }')
