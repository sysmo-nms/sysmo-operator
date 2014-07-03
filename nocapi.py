import noctopus_main
import noctopus_ramp
import noctopus_images

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
    return noctopus_main.NMainWindow.singleton.activeProxySettings

def nGetViewMode():
    ''' return:
    {
        'screen':   'full' | 'normal',
        'mode':     'minimal' | 'simple' | 'expert',
        'tray':     'traymin' | 'traymax'
    }
    '''
    return noctopus_main.NMainWindow.singleton.activeViewMode

def nGetPixmap(pixmapName):
    ''' return:
        PySide.QtGui.QPixmap()
    '''
    return noctopus_images.getPixmap(pixmapName)

def nGetIcon(iconName):
    ''' return:
        PySide.QtGui.QIcon()
    '''
    return noctopus_images.getIcon(iconName)

def nGetImage(imageName):
    ''' return:
        str = path to svg file
    '''
    return noctopus_images.getImage(imageName)

def nGetRgb(paletteKey):
    ''' return:
        str = "%R%G%B"
    '''
    return noctopus_images.getRgb(paletteKey)

def nGetRgba(paletteKey):
    ''' return:
        str = "%R%G%B%A"
    '''
    return noctopus_images.getRgba(paletteKey)

def nConnectProxySettings(pyCallable):
    ''' return: None
    Connect every proxy settings modification to the pyCallable given as 
    argument.
    pyCallable will receive: Signal(dict)
    {
        'use':  True | False,
        'host': str,
        'port': int
    }
    '''
    return noctopus_main.NMainWindow.singleton.proxySettings.connect(pyCallable)

def nConnectViewMode(pyCallable):
    ''' return: None
    Connect every view mode modification to the pyCallable given as argument.
    pyCallable will receive: Signal(dict)
    {
        'screen':   'full' | 'normal',
        'mode':     'minimal' | 'simple' | 'expert',
        'tray':     'traymin' | 'traymax'
    }
    '''
    noctopus_main.NMainWindow.singleton.viewMode.connect(pyCallable)

def nConnectAppToggled(pyCallable):
    ''' return: None
    Connect every toggle event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is already visible.
    pyCallable will receive: {'button': 'left'|'right', 'id': 'appname'}.
    '''
    noctopus_ramp.NSelector.singleton.appButtonToggled.connect(pyCallable)
    return None

def nConnectAppSelect(pyCallable):
    ''' return: None
    Connect every select event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is not visible.
    pyCallable will receive: str, when str = module name. Signal(str)
    '''
    noctopus_ramp.NSelector.singleton.appButtonPressed.connect(pyCallable)
    return None

def nConnectWillClose(pyCallable):
    ''' return: None
    Connect the close event to pyCallable.
    module button from the ramp is pressed, wille the module is not
    visible.
    pyCallable will receive nothing. Signal()
    '''
    noctopus_main.NMainWindow.singleton.willClose.connect(pyCallable)
    return None

def nSetStatusMsg(msg):
    ''' return: None
        Set a message to the statusbar.
    '''
    return noctopus_main.NMainWindow.singleton.statusBar.showMessage(msg)
    return None

def nSetMessageProcessor(key, pyCallable):
    ''' return: None
        Set the supercast message processor for messages from key.
    '''
    noctopus_main.NMainWindow.singleton.supercast.setMessageProcessor(key,pyCallable)
    return None

def nConnectSupercastEnabled(pyCallable):
    '''
        Emit when noctopus + supercast have finished their initialisation 
        (the user is logged in).
    '''
    noctopus_main.NMainWindow.singleton.supercastEnabled.connect(pyCallable)

def nSubscribe(pyCallable, channel):
    '''
        Subscribe to a supercast channel.
    '''
    noctopus_main.NMainWindow.singleton.supercast.subscribe(pyCallable, channel)

def nUnsubscribe(pyCallable, channel):
    '''
        Unsubscribe to a supercast channel.
    '''
    noctopus_main.NMainWindow.singleton.supercast.unsubscribe(pyCallable, channel)

def nQuery(key, callback):
    sc = noctopus_main.NMainWindow.singleton.supercast
    sc.send('query', key, callback)

def nGetGroups():
    sc = noctopus_main.NMainWindow.singleton.supercast
    return sc.groups

def nAddMainMenu(menu):
    mw = noctopus_main.NMainWindow.singleton
    mw.setApplicationMenu(menu)
