from    PyQt5.QtGui    import (
    QPalette
)
from    PyQt5.QtWidgets    import (
    QTreeView,
    QFrame,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSlider,
    QButtonGroup,
    QStackedLayout,
    QScrollArea
)

from PyQt5.QtCore import Qt
from noctopus_widgets   import (
    NFrame,
    NFrameContainer,
    NGridContainer,
    NGrid,
    NInfoButton
)

import nocapi


class Timeline(NFrame):
    def __init__(self, parent):
        super(Timeline, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._grid = NGrid(self)
        self.setLayout(self._grid)
        self._commands    = TimelineCommands(self)
        self._timestack   = TimelineStack(self)
        self._timeslide = TimelineSlide(self)
        self._commands.stackGroup.buttonClicked[int].connect(self._timestack.stack.setCurrentIndex)
        self._commands.minimizeButton.clicked.connect(self._updateLayout)
        self._timeslide.minimizeButton.clicked.connect(self._updateLayout)

        self._minimized = True
        #self.setDisabled(True)
        self._initLayout()

    def _initLayout(self):
        if self._minimized == False:
            self._setWideLayout()
        else:
            self._setMinLayout()

    def _updateLayout(self):
        if self._minimized == False:
            self._setMinLayout()
        else:
            self._setWideLayout()

    def _setWideLayout(self):
        self._commands.hideControls(True)
        self._commands.show()
        self._timestack.show()
        self._timeslide.show()
        self._grid.addWidget(self._commands,      0,0)
        self._grid.addWidget(self._timestack,     1,0)
        self._grid.addWidget(self._timeslide,     2,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self._grid.setRowStretch(2,0)
        self._grid.setRowStretch(3,0)
        self._minimized = False

    def _setMinLayout(self):
        self._commands.hideControls(False)
        self._commands.show()
        self._timestack.hide()
        self._timeslide.hide()
        self._grid.addWidget(self._commands, 0,0)
        self._minimized = True


class TimelineCommands(NFrameContainer):
    def __init__(self, parent):
        super(TimelineCommands, self).__init__(parent)
        # minimize
        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(nocapi.nGetIcon('go-up'))
        self.minimizeButton.setToolTip('minimize')

        self.sep0 = QFrame(self)
        self.sep0.setFixedWidth(6)
        self.sep0.setFrameShape(QFrame.NoFrame)
        self.sep0.setFrameShadow(QFrame.Plain)

        self.minimizeButton.hide()
        self.sep0.hide()
        
        # stack control commands
        self.stackGroup = QButtonGroup(self)
        self.stackGroup.setExclusive(True)

        timeStack = QPushButton(self)
        timeStack.setIcon(nocapi.nGetIcon('appointment-new'))
        timeStack.setCheckable(True)

        textStack = QPushButton(self)
        textStack.setIcon(nocapi.nGetIcon('edit-paste'))
        textStack.setCheckable(True)

        self.stackGroup.addButton(timeStack, 0)
        self.stackGroup.addButton(textStack, 1)
        timeStack.setChecked(True)

        # separator
        sep1 = QFrame(self)
        sep1.setFixedWidth(6)
        sep1.setFrameShape(QFrame.NoFrame)
        sep1.setFrameShadow(QFrame.Plain)

        # search commands
        clearButton = QPushButton(self)
        clearButton.setIcon(nocapi.nGetIcon('edit-clear'))
        searchLine  = QLineEdit(self)


        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)
        grid.addWidget(self.minimizeButton, 0,0)
        grid.addWidget(self.sep0,      0,1)
        grid.addWidget(timeStack,   0,2)
        grid.addWidget(textStack,   0,3)
        grid.addWidget(sep1,        0,4)
        grid.addWidget(clearButton, 0,5)
        grid.addWidget(searchLine,  0,6)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,0)
        grid.setColumnStretch(4,0)
        grid.setColumnStretch(5,0)
        grid.setColumnStretch(6,1)
        grid.setColumnStretch(7,3)
        self.setLayout(grid)

    def hideControls(self, boo):
        if boo == True:
            self.sep0.hide()
            self.minimizeButton.hide()
        else:
            self.sep0.show()
            self.minimizeButton.show()
            
    def _minimizeClicked(self):
        print("minimize!")

class TimelineStack(NFrameContainer):
    def __init__(self, parent):
        super(TimelineStack, self).__init__(parent)
        self.stack = QStackedLayout(self)
        self._text = TimelineText(self)
        self._draw = TimelineDraw(self)
        self.stack.insertWidget(0, self._draw)
        self.stack.insertWidget(1, self._text)
        self.setLayout(self.stack)
        self.stack.setCurrentIndex(0)
        

class TimelineSlide(NFrameContainer):
    def __init__(self, parent):
        super(TimelineSlide, self).__init__(parent)
        grid = NGridContainer(self)

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(nocapi.nGetIcon('go-down'))
        self.minimizeButton.setToolTip('minimize')

        sep0 = QFrame(self)
        sep0.setFixedWidth(6)
        sep0.setFrameShape(QFrame.NoFrame)
        sep0.setFrameShadow(QFrame.Plain)

        slide = QSlider(Qt.Horizontal, self)
        grid.addWidget(self.minimizeButton, 0,0)
        grid.addWidget(sep0,                0,1)
        grid.addWidget(slide,               0,2)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,1)
        self.setLayout(grid)

class TimelineText(QTextEdit):
    def __init__(self, parent):
        super(TimelineText, self).__init__(parent)

class TimelineDraw(QScrollArea):
    def __init__(self, parent):
        super(TimelineDraw, self).__init__(parent)
        layout = NGridContainer(self)
        layout.addWidget(QLabel('draw', self), 0,0)
        self.setLayout(layout)
