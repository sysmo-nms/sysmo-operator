import sysmo_main
import sysmo_images

######################
# MODULES API HELPER #
######################
def nGetProxySettings():
    ''' return:
    {
        'use': True | False,
        'host': str,
        'port': int
    }
    '''
    return sysmo_main.NMainWindow.singleton.activeProxySettings

def nGetViewMode():
    ''' return:
    {
        'screen':   'full' | 'normal',
        'mode':     'minimal' | 'simple' | 'expert',
        'tray':     'traymin' | 'traymax'
    }
    '''
    return sysmo_main.NMainWindow.singleton.activeViewMode

def nGetPixmap(pixmapName):
    ''' return:
        PyQt5.QtGui.QPixmap()
    '''
    return sysmo_images.getPixmap(pixmapName)

def nGetIcon(iconName):
    ''' return:
        PyQt5.QtGui.QIcon()
    '''
    return sysmo_images.getIcon(iconName)

def nGetImage(imageName):
    ''' return:
        str = path to svg file
    '''
    return sysmo_images.getImage(imageName)

def nGetRgb(paletteKey):
    ''' return:
        str = "%R%G%B"
    '''
    return sysmo_images.getRgb(paletteKey)

def nGetRgba(paletteKey):
    ''' return:
        str = "%R%G%B%A"
    '''
    return sysmo_images.getRgba(paletteKey)

def nConnectProxySettings(pyCallable):
    ''' return: None
    Connect every proxy settings modification to the pyCallable given as 
    argument.
    pyCallable will receive: pyqtSignal(dict)
    {
        'use':  True | False,
        'host': str,
        'port': int
    }
    '''
    return sysmo_main.NMainWindow.singleton.proxySettings.connect(pyCallable)

def nConnectAppToggled(pyCallable):
    ''' return: None
    Connect every toggle event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is already visible.
    pyCallable will receive: {'button': 'left'|'right', 'id': 'appname'}.
    '''
    sysmo_main.NSelector.singleton.appButtonToggled.connect(pyCallable)
    return None

def nConnectAppSelect(pyCallable):
    ''' return: None
    Connect every select event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is not visible.
    pyCallable will receive: str, when str = module name. pyqtSignal(str)
    '''
    sysmo_main.NSelector.singleton.appButtonPressed.connect(pyCallable)
    return None

def nConnectWillClose(pyCallable):
    ''' return: None
    Connect the close event to pyCallable.
    module button from the ramp is pressed, wille the module is not
    visible.
    pyCallable will receive nothing. pyqtSignal()
    '''
    sysmo_main.NMainWindow.singleton.willClose.connect(pyCallable)
    return None

def nSetStatusMsg(msg):
    ''' return: None
        Set a message to the statusbar.
    '''
    return sysmo_main.NMainWindow.singleton.statusBar.showMessage(msg)
    return None

def nSetMessageProcessor(key, pyCallable):
    ''' return: None
        Set the supercast message processor for messages from key.
    '''
    sysmo_main.NMainWindow.singleton.supercast.setMessageProcessor(key,pyCallable)
    return None

def nConnectSupercastEnabled(pyCallable):
    '''
        Emit when sysmo + supercast have finished their initialisation 
        (the user is logged in).
    '''
    sysmo_main.NMainWindow.singleton.supercastEnabled.connect(pyCallable)

def nSubscribe(pyCallable, channel):
    '''
        Subscribe to a supercast channel.
    '''
    sysmo_main.NMainWindow.singleton.supercast.subscribe(pyCallable, channel)

def nUnsubscribe(pyCallable, channel):
    '''
        Unsubscribe to a supercast channel.
    '''
    sysmo_main.NMainWindow.singleton.supercast.unsubscribe(pyCallable, channel)

def nQuery(key, callback):
    sc = sysmo_main.NMainWindow.singleton.supercast
    sc.send('query', key, callback)

def nGetGroups():
    sc = sysmo_main.NMainWindow.singleton.supercast
    return sc.groups

def nAddMainMenu(menu):
    mw = sysmo_main.NMainWindow.singleton
    mw.setApplicationMenu(menu)

def nGetSystemTrayIcon():
    return sysmo_main.NMainWindow.singleton._trayIcon
