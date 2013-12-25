from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    WorkingProbeView    import ProbeView


class TargetView(QFrame):
    def __init__(self, parent, target, probe):
        super(TargetView, self).__init__(parent)
        self.probeViews = dict()
        self.rowCount   = 1

        self.targetHead  = TargetHead(self, target)
        self.targetBody  = TargetBody(self)
        self.targetBodyGrid = QGridLayout(self)
        self.targetBody.setLayout(self.targetBodyGrid)

        tab         = QFrame(self)
        tab.setFixedWidth(10)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.targetHead, 0,0,1,2)
        self.grid.addWidget(tab,                      1,0)
        self.grid.addWidget(self.targetBody, 1,1)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.setLayout(self.grid)
        self.newProbe(probe)

    def toggleBody(self):
        if self.grid.itemAtPosition(1,1) == None:
            self.grid.addWidget(self.targetBody, 1, 1)
        else:
            self.grid.removeWidget(self.targetBody)

    def newProbe(self, probe):
        self.probeViews[probe] = ProbeView(self, probe)
        self.targetBodyGrid.addWidget(self.probeViews[probe], self.rowCount, 1)
        self.rowCount += 1

    def removeProbe(self, probe):
        self.targetBodyGrid.removeWidget(self.probeViews[probe])
        self.probeViews[probe].deleteLater()
        self.targetBodyGrid.update()
        del self.probeViews[probe]
        if len(self.probeViews) == 0:
            return 'empty'
        else:
            return 'full'

class TargetHead(QFrame):
    def __init__(self, parent, target):
        super(TargetHead, self).__init__(parent)
        #self.setBackgroundRole(QPalette.Window)
        #self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.toggleButton = QPushButton('Toggle', self)
        self.toggleButton.clicked.connect(parent.toggleBody)

        self.summary    = TargetProbeOverallSummary(self)

        self.promoteCheck = QCheckBox('include in Dashboard', self)

        grid = QGridLayout(self)
        grid.addWidget(self.toggleButton,    0,0)
        grid.addWidget(QLabel(target, self), 0,1)
        grid.addWidget(self.summary,         0,2)
        grid.addWidget(self.promoteCheck,    0,4)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,1)
        grid.setColumnStretch(4,0)
        self.setLayout(grid)

class TargetBody(QFrame):
    def __init__(self, parent):
        super(TargetBody, self).__init__(parent)


# class Window(QtGui.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
# 
#         flowLayout = FlowLayout()
#         flowLayout.addWidget(QtGui.QPushButton("Short"))
#         flowLayout.addWidget(QtGui.QPushButton("Longer"))
#         flowLayout.addWidget(QtGui.QPushButton("Different text"))
#         flowLayout.addWidget(QtGui.QPushButton("More text"))
#         flowLayout.addWidget(QtGui.QPushButton("Even longer button text"))
#         self.setLayout(flowLayout)
# 
#         self.setWindowTitle("Flow Layout")


class ProbeCriticalButton(QPushButton):
    def __init__(self, parent):
        super(ProbeCriticalButton, self).__init__(parent)
        self.setText('   critical: check-qqchose   ')
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
                stop: 0 #ef2929,    \
                stop: 1 #cc0000);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #a40000;      \
        }')

class ProbeWarningButton(QPushButton):
    def __init__(self, parent):
        super(ProbeWarningButton, self).__init__(parent)
        self.setText('   warning: check-qqchose   ')
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
        }')

class ProbeOkButton(QPushButton):
    def __init__(self, parent):
        super(ProbeOkButton, self).__init__(parent)
        self.setText('   ok: check-qqchose   ')
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
                stop: 0 #a1d99b,    \
                stop: 1 #74c476);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #41ab5d;      \
        }')

class TargetProbeSummaryWidget(QLabel):
    def __init__(self, parent):
        super(TargetProbeSummary, self).__init__(parent)

class TargetProbeOverallSummary(QFrame):
    def __init__(self, parent):
        super(TargetProbeOverallSummary, self).__init__(parent)
        self.setFixedWidth(500)
        layout = FlowLayout(self)

        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeCriticalButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeOkButton(self))
        layout.addWidget(ProbeWarningButton(self))
        layout.addWidget(ProbeOkButton(self))

        self.setLayout(layout)

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        # XXX
        #if parent is not None:
            #self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        # XXX
        #size += QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
