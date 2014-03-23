# Python
from functools import partial
# PySide
from    PySide.QtGui    import (
    QAction,
    QActionGroup
)

from noctopus_images import getIcon

def initMenus(mainWin):
    " Menu bar "
    "File"
    menu = mainWin.menuBar()
    menuFile    = menu.addMenu('Noctopus')
    exitAction  = QAction(getIcon('system-log-out'), '&Exit', mainWin)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(mainWin.close)
    menuFile.addAction(exitAction)

    "Win"
    fullScreenAction  = QAction(
        getIcon('video-display'), '&Full screen', mainWin)
    fullScreenAction.setShortcut('Ctrl+F')
    fullScreenAction.triggered.connect(mainWin._toggleFullScreen)

    actionSimpleView    = QAction('Simplified view', mainWin)
    actionSimpleView.setCheckable(True)
    actionSimpleView.triggered.connect(mainWin._setSimpleView)

    actionMinimalView    = QAction('Minimal view', mainWin)
    actionMinimalView.setCheckable(True)
    actionMinimalView.triggered.connect(mainWin._setMinimalView)

    actionExpertView    = QAction('Expert view', mainWin)
    actionExpertView.setCheckable(True)
    actionExpertView.triggered.connect(mainWin._setExpertView)
    actionExpertView.setChecked(True)

    toggleSimpleView    = QActionGroup(mainWin)
    toggleSimpleView.addAction(actionMinimalView)
    toggleSimpleView.addAction(actionSimpleView)
    toggleSimpleView.addAction(actionExpertView)
    toggleSimpleView.setExclusive(True)

    menuWin     = menu.addMenu('Views')
    menuWin.addAction(actionMinimalView)
    menuWin.addAction(actionSimpleView)
    menuWin.addAction(actionExpertView)
    menuWin.addSeparator()
    menuWin.addAction(fullScreenAction)

    " configure menu "

    actionConfigureProxy = QAction('Proxy settings', mainWin)
    actionConfigureProxy.triggered.connect(mainWin._launchProxySettings)

    menuConf    = menu.addMenu('Configure')
    menuConf.addAction(actionConfigureProxy)

    " style menu "
    nativeAction    = QAction('Native', mainWin)
    nativeAction.setCheckable(True)
    nativeAction.triggered.connect(partial(mainWin._setStyle, 'Native'))

    plastiqueAction = QAction('plastique', mainWin)
    plastiqueAction.setCheckable(True)
    plastiqueAction.triggered.connect(partial(mainWin._setStyle, 'plastique'))

    cdeAction       = QAction('cde', mainWin)
    cdeAction.setCheckable(True)
    cdeAction.triggered.connect(partial(mainWin._setStyle, 'cde'))

    motifAction     = QAction('motif', mainWin)
    motifAction.setCheckable(True)
    motifAction.triggered.connect(partial(mainWin._setStyle, 'motif'))

    windowAction    = QAction('windows classic', mainWin)
    windowAction.setCheckable(True)
    windowAction.triggered.connect(partial(mainWin._setStyle, 'window'))

    windowxpAction  = QAction('windows xp', mainWin)
    windowxpAction.setCheckable(True)
    windowxpAction.triggered.connect(partial(mainWin._setStyle, 'windowxp'))

    styleToggle = QActionGroup(mainWin)
    styleToggle.addAction(plastiqueAction)
    styleToggle.addAction(nativeAction)
    styleToggle.addAction(cdeAction)
    styleToggle.addAction(motifAction)
    styleToggle.addAction(windowAction)
    styleToggle.addAction(windowxpAction)
    styleToggle.setExclusive(True)
    plastiqueAction.setChecked(True)

    menuStyle = menu.addMenu('Style')
    menuStyle.addAction(nativeAction)
    menuStyle.addAction(plastiqueAction)
    menuStyle.addAction(cdeAction)
    menuStyle.addAction(motifAction)
    menuStyle.addAction(windowAction)
    menuStyle.addAction(windowxpAction)

    return
