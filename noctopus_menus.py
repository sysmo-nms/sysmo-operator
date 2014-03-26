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
    exitAction  = QAction(getIcon('system-log-out'), mainWin.tr('&Exit'), mainWin)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(mainWin.close)
    menuFile.addAction(exitAction)

    "Win"
    fullScreenAction  = QAction(
        getIcon('video-display'), mainWin.tr('&Full screen'), mainWin)
    fullScreenAction.setShortcut('Ctrl+F')
    fullScreenAction.triggered.connect(mainWin._toggleFullScreen)

    actionSimpleView    = QAction(mainWin.tr('Simplified view'), mainWin)
    actionSimpleView.setCheckable(True)
    actionSimpleView.triggered.connect(mainWin._setSimpleView)

    actionMinimalView    = QAction(mainWin.tr('Minimal view'), mainWin)
    actionMinimalView.setCheckable(True)
    actionMinimalView.triggered.connect(mainWin._setMinimalView)

    actionExpertView    = QAction(mainWin.tr('Expert view'), mainWin)
    actionExpertView.setCheckable(True)
    actionExpertView.triggered.connect(mainWin._setExpertView)
    actionExpertView.setChecked(True)

    toggleSimpleView    = QActionGroup(mainWin)
    toggleSimpleView.addAction(actionMinimalView)
    toggleSimpleView.addAction(actionSimpleView)
    toggleSimpleView.addAction(actionExpertView)
    toggleSimpleView.setExclusive(True)

    menuWin     = menu.addMenu(mainWin.tr('Views'))
    menuWin.addAction(actionMinimalView)
    menuWin.addAction(actionSimpleView)
    menuWin.addAction(actionExpertView)
    menuWin.addSeparator()
    menuWin.addAction(fullScreenAction)

    " configure menu "

    actionConfigureProxy = QAction(mainWin.tr('Proxy settings'), mainWin)
    actionConfigureProxy.triggered.connect(mainWin._launchProxySettings)

    menuConf    = menu.addMenu(mainWin.tr('Configure'))
    menuConf.addAction(actionConfigureProxy)

    " style menu "
    nativeAction    = QAction(mainWin.tr('Native'), mainWin)
    nativeAction.setCheckable(True)
    nativeAction.triggered.connect(partial(mainWin._setStyle, 'Native'))

    plastiqueAction = QAction(mainWin.tr('plastique'), mainWin)
    plastiqueAction.setCheckable(True)
    plastiqueAction.triggered.connect(partial(mainWin._setStyle, 'Plastique'))

    cleanlooksAction = QAction(mainWin.tr('cleanlooks'), mainWin)
    cleanlooksAction.setCheckable(True)
    cleanlooksAction.triggered.connect(partial(mainWin._setStyle, 'Cleanlooks'))

    cdeAction       = QAction(mainWin.tr('cde'), mainWin)
    cdeAction.setCheckable(True)
    cdeAction.triggered.connect(partial(mainWin._setStyle, 'CDE'))

    motifAction     = QAction(mainWin.tr('motif'), mainWin)
    motifAction.setCheckable(True)
    motifAction.triggered.connect(partial(mainWin._setStyle, 'Motif'))

    windowAction    = QAction(mainWin.tr('windows classic'), mainWin)
    windowAction.setCheckable(True)
    windowAction.triggered.connect(partial(mainWin._setStyle, 'Windows'))

    windowxpAction  = QAction(mainWin.tr('windows xp'), mainWin)
    windowxpAction.setCheckable(True)
    windowxpAction.triggered.connect(partial(mainWin._setStyle, 'WindowXP'))

    styleToggle = QActionGroup(mainWin)
    styleToggle.addAction(plastiqueAction)
    styleToggle.addAction(cleanlooksAction)
    styleToggle.addAction(nativeAction)
    styleToggle.addAction(cdeAction)
    styleToggle.addAction(motifAction)
    styleToggle.addAction(windowAction)
    styleToggle.addAction(windowxpAction)
    styleToggle.setExclusive(True)

    print "style is ", mainWin._noctopusStyle
    if mainWin._noctopusStyle == 'Native':
        nativeAction.setChecked(True)
    elif mainWin._noctopusStyle == 'Plastique':
        plastiqueAction.setChecked(True)
    elif mainWin._noctopusStyle == 'Cleanlooks':
        cleanlooksAction.setChecked(True)
    elif mainWin._noctopusStyle == 'CDE':
        cdeAction.setChecked(True)
    elif mainWin._noctopusStyle == 'Motif':
        motifAction.setChecked(True)
    elif mainWin._noctopusStyle == 'Windows':
        windowAction.setChecked(True)
    elif mainWin._noctopusStyle == 'WindowXP':
        windowxpAction.setChecked(True)
    else:
        plastiqueAction.setChecked(True)

    menuStyle = menu.addMenu(mainWin.tr('Style'))
    menuStyle.addAction(nativeAction)
    menuStyle.addAction(plastiqueAction)
    menuStyle.addAction(cleanlooksAction)
    menuStyle.addAction(cdeAction)
    menuStyle.addAction(motifAction)
    menuStyle.addAction(windowAction)
    menuStyle.addAction(windowxpAction)

    return
