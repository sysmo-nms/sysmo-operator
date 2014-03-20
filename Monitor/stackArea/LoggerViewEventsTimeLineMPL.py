from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    matplotlib          import pyplot
import  TkorderMain
import  matplotlib          as mpl

class SimpleTimeLine(QFrame):
    def __init__(self, parent):
        super(SimpleTimeLine, self).__init__(parent)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0,0,0,0)

        self.dpiWidth = TkorderMain.TkorderClient.singleton.dpiWidth
        self.dpiHeight = TkorderMain.TkorderClient.singleton.dpiHeight

        grid = QGridLayout(self)
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        self.figureLabel = QLabel(self)
        self.initFigure()
        pixmap = QPixmap(self.figureFileName)
        self.figureLabel.setPixmap(pixmap)
        grid.addWidget(self.figureLabel, 0,0)
        self.setLayout(grid)

    def initFigure(self):
        self.figureFile = QTemporaryFile(self)
        self.figureFile.open()
        self.figureFile.close()
        self.figureFileName = self.figureFile.fileName()

        fig = pyplot.figure(figsize=(8,1), dpi=96, frameon=False)
        ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])

        # Set the colormap and norm to correspond to the data for which
        # the colorbar will be used.
        cmap = mpl.cm.cool
        norm = mpl.colors.Normalize(vmin=5, vmax=10)
        
        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                   norm=norm,
                                   orientation='horizontal')
        cb1.set_label('Some Units')
        print self.figureFileName
        pyplot.savefig(self.figureFileName, format='png', dpi=70)

