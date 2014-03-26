# from    PySide.QtCore   import *
# from    PySide.QtGui    import *
# from    noctopus_widgets     import NFrameContainer, NGridContainer
# import  nocapi
# 
# class Commands(NFrameContainer):
#     def __init__(self, parent):
#         super(Commands, self).__init__(parent)
#         grid = NGridContainer(self)
#         self.addButton = QPushButton(nocapi.nGetIcon('list-add'), 'Add', self)
#         self.addButton.clicked.connect(self._launchWizard)
#         grid.addWidget(self.addButton, 0,0)
#         grid.setColumnStretch(0,0)
#         grid.setColumnStretch(1,1)
#         self.setLayout(grid)
# 
#     def _launchWizard(self):
#         wizard = AddTargetWizard(self)
