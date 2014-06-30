from    PySide.QtGui    import (
    QToolBox,
    QDialog,
    QWidget,
    QLabel,
    QWindowsStyle,
    QPlastiqueStyle,
    QCleanlooksStyle,
    QGtkStyle,
    QMotifStyle,
    QCDEStyle,
    QStyle
)

from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    QLabel
)

import  nocapi
import  opus.monitor.api    as monapi

def openPropertiesFor(element):
    if element not in Properties.Elements.keys():
        v = Properties(element)
        Properties.Elements[element] = v
    else:
        Properties.Elements[element].show()
        
    
class Properties(QDialog):
    Elements = dict()
    def __init__(self, element, parent = None):
        super(Properties, self).__init__()
        print "jojo prop: ", element
        self.setWindowTitle("hohoo")
        grid = NGridContainer(self)
        toolbox = QToolBox(self)
#         toolbox.setStyleSheet('''QToolBox::tab {
#              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                                  stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
#                                  stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
#      border-radius: 5px;
#      color: darkgray;
#         };
#         QToolBox::tab::selected {
#                  font: italic;
#      color: white;
#         }''')
        toolbox.addItem(QLabel('item1', self), 'item1')
        toolbox.addItem(QLabel('item2', self), 'item2')
        toolbox.addItem(QLabel('item3', self), 'item3')
        toolbox.addItem(QLabel('item4', self), 'item4')
        grid.addWidget(toolbox, 0,0)
        self.setLayout(grid)
        self.show()




