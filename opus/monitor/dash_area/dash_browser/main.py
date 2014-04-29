from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer
)
from    opus.monitor.widgets                import TextLog
from    opus.monitor.dash_area.dash_widgets import DashTreeWidget

class BrowserDash(NFrameContainer):
    def __init__(self, parent):
        super(BrowserDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        dashWidget = DashTreeWidget(self)
        dashWidget.setDashLabels('Elements', 'Text logs')
        dashWidget.setItemWidgetClass(TextLog)
        self._grid.addWidget(dashWidget, 0,0)
        self.setLayout(self._grid)
