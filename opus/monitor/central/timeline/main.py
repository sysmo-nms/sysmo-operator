from    PySide.QtGui    import (
    QTreeView,
    QFrame,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSlider,
    QPalette,
    QButtonGroup,
    QStackedLayout,
    QScrollArea
)

from PySide.QtCore import Qt
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
        commands = TimelineCommands(self)
        timestack = TimelineStack(self)
        timeslide = TimelineSlide(self)
        commands.stackGroup.buttonClicked[int].connect(timestack.stack.setCurrentIndex)
        self._grid.addWidget(commands,      0,0)
        self._grid.addWidget(timestack,     1,0)
        self._grid.addWidget(timeslide,     2,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self._grid.setRowStretch(2,0)
        self.setLayout(self._grid)

class TimelineCommands(NFrameContainer):
    def __init__(self, parent):
        super(TimelineCommands, self).__init__(parent)
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
        sep = QFrame(self)
        sep.setFixedWidth(6)
        sep.setFrameShape(QFrame.NoFrame)
        sep.setFrameShadow(QFrame.Plain)

        # search commands
        clearButton = QPushButton(self)
        clearButton.setIcon(nocapi.nGetIcon('edit-clear'))
        searchLine  = QLineEdit(self)


        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)
        grid.addWidget(timeStack,   0,0)
        grid.addWidget(textStack,   0,1)
        grid.addWidget(sep,         0,2)
        grid.addWidget(clearButton, 0,3)
        grid.addWidget(searchLine,  0,4)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,0)
        grid.setColumnStretch(4,1)
        grid.setColumnStretch(5,3)
        self.setLayout(grid)

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
        slide = QSlider(Qt.Horizontal, self)
        grid.addWidget(slide, 0,0)
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
