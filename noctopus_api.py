import noctopus
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
        
    return noctopus.NMainWindow.singleton.getProxySettings()

def nGetViewMode():

    ''' return:
    {
        'screen':   'full' | 'normal',
        'mode':     'minimal' | 'simple' | 'expert',
        'tray':     'traymin' | 'traymax'
    }
    '''
    return noctopus.NMainWindow.singleton.getViewMode()

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

def nConnectProxySettings(pyCallable):

    ''' return: nothing
    Connect every proxy settings modification to the pyCallable given as 
    argument.
    pyCallable will receive: Signal(dict)
    {
        'use':  True | False,
        'host': str,
        'port': int
    }
    '''

    return noctopus.NMainWindow.singleton.proxySettings.connect(pyCallable)

def nConnectViewMode(pyCallable):

    ''' return: True
    Connect every view mode modification to the pyCallable given as argument.
    pyCallable will receive: Signal(dict)
    {
        'screen':   'full' | 'normal',
        'mode':     'minimal' | 'simple' | 'expert',
        'tray':     'traymin' | 'traymax'
    }
    '''

    noctopus.NMainWindow.singleton.viewMode.connect(pyCallable)
    return True

def nConnectAppToggle(pyCallable):

    ''' return: True
    Connect every toggle event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is already visible.
    pyCallable will receive: str, when str = module name. Signal(str)
    '''

    noctopus.NSelector.singleton.appButtonToggle.connect(pyCallable)
    return True

def nConnectAppSelect(pyCallable):

    ''' return: True
    Connect every select event from the left ramp buttons to pyCallable.
    Trigered when a module button from the ramp is pressed, wille the module
    is not visible.
    pyCallable will receive: str, when str = module name. Signal(str)
    '''

    noctopus.NSelector.singleton.appButtonPressed.connect(pyCallable)
    return True

def nConnectWillClose(pyCallable):

    ''' return: True
    Connect the close event to pyCallable.
    module button from the ramp is pressed, wille the module is not
    visible.
    pyCallable will receive nothing. Signal()
    '''

    noctopus.NMainWindow.singleton.willClose.connect(pyCallable)
    return True

def nSetStatusMsg(msg):

    ''' return: None
        Set a message to the statusbar.
    '''
    return noctopus.NMainWindow.singleton.setStatusMsg(msg)
