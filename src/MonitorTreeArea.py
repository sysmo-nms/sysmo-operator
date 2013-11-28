from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    MonitorEvents   import ChannelHandler
import  TkorderIcons


#####################################################################
#####################################################################
###### LEFT PANNEL VIEW #############################################
#####################################################################
#####################################################################
class TreeContainer(QFrame):
    
    " the left tree area. Emit user clics events"

    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self.trackerMain  = parent

        self.treeview   = MonitorTView(self)
        self.searchBar  = MonitorTreeSearch(self)
        self.info       = MonitorTreeAreaInfo(self)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(5)
        grid.addWidget(self.searchBar,          1, 0)
        grid.addWidget(self.treeview,           2, 0)
        grid.addWidget(self.info,               3, 0)

        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,0)

        self.setLayout(grid)
        self.setMaximumWidth(500)

class MonitorTreeSearch(QFrame):
    def __init__(self, parent):
        super(MonitorTreeSearch, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(0)
        clear   = QPushButton(self)
        line    = QLineEdit(self)
        clear.setIcon(TkorderIcons.get('edit-clear'))
        line.setPlaceholderText('Filter')
        grid.addWidget(clear,   0,0)
        grid.addWidget(line,    0,1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        self.setLayout(grid)


class MonitorTreeButtons(QToolBar):
    def __init__(self, parent):
        super(MonitorTreeButtons, self).__init__(parent)
        self.addAction(TkorderIcons.get('applications-development'), 'Debug', self.hello())

    def hello(self): pass

class MonitorTreeAreaInfo(QTextEdit):
    def __init__(self, parent):
        super(MonitorTreeAreaInfo, self).__init__(parent)
        # text document
        dtext   = QTextDocument()
        dtext.setMaximumBlockCount(500)
        tformat = QTextCharFormat()
        tformat.setFontPointSize(8.2)

        # QTextEdit config
        self.setDocument(dtext)
        self.setCurrentCharFormat(tformat)
        self.setReadOnly(True)
        #self.setStyleSheet(
            #"QTextEdit { \
                #border-radius: 10px;\
                #background: #F9EE75 \
            #}")
        self.setFixedHeight(100)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShadow(QFrame.Raised)

        # signals to receive
        sigDict = ChannelHandler.singleton.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._informational)
        sigDict['targetInfo'].signal.connect(self._informational)
        sigDict['probeModInfo'].signal.connect(self._informational)

    def _informational(self, msg):
        self.append(str(msg))


###############################################################################
#### PROTOTYPE POUR TREEVIEW ##################################################
###############################################################################
class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()        

# Nous allons creer une classe mere de nos futurs modeles
# pour limiter la complexite et gerer ce que l'on peut gerer en amont :
class TreeModel(QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()

    # a implementer par la future classe fille
    def _getRootNodes(self):
        raise NotImplementedError()
    
    # cette methode heritee de QAbstractItemModel doit retourner
    # l'indice de l'enregistrement en entree moyennant le parent (un QModelIndex)
    # c.f. paragraph suivant pour plus d'explications.
    def index(self, row, column, parent):
        # si l'indice du parent est invalide
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])

    # cette methode heritee de QAbstractItemModel doit retourner
    # l'indice du parent de l'indice donne en parametre
    # ou un indice invalide (QModelIndex()) si le noeud n'a pas de parent
    # ou si la requete est incorrecte
    # c.f. paragraph suivant pour plus d'explications.
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        # on recupere l'objet sous-jacent avec la methode internalPointer de l'indice
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            # si tout est valide alors on cree l'indice associe pointant vers le parent
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        QAbstractItemModel.reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)



##############################################################################
### TREEVIEW #################################################################
##############################################################################
class MonitorTView(QTreeView):
    def __init__(self, parent):
        super(MonitorTView, self).__init__(parent)
        model = NamesModel()
        self.setModel(model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setModel(model)
            
class NamedElement(object): # notre structure interne pour gerer les objets
    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements

# notre noeud concret implementant getChildren
class NamedNode(TreeNode):
    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

    # renvoie la liste des noeuds fils en utilisant la liste subelements de 
    # notre objet (interne) NamedElement
    def _getChildren(self):
        return [NamedNode(elem, self, index)
            for index, elem in enumerate(self.ref.subelements)]
        
# et enfin notre modele avec 
class NamesModel(TreeModel):
    def __init__(self, rootElements):
        self.rootElements = rootElements
        TreeModel.__init__(self)

    def _getRootNodes(self):
        return [NamedNode(elem, None, index)
            for index, elem in enumerate(self.rootElements)]

    def columnCount(self, parent):
        return 1

    # permet de recuperer les donnees liees a un indice et un role.
    # ces donnees peuvent ainsi varier selon le role.
    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.ref.name
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole \
            and section == 0:
            return 'Name'
        return None
            

