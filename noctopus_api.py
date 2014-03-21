import noctopus
import noctopus_images

######################
# MODULES API HELPER #
######################
def nGetProxySettings():
    return noctopus.NMainWindow.singleton.getProxySettings()

def nGetViewMode():
    return noctopus.NMainWindow.singleton.getViewMode()

def nGetIcon(iconName):
    return noctopus_images.getIcon(iconName)

def nGetImage(imageName):
    return noctopus_images.getImage(imageName)

def nConnectProxySettings(pyCallable):
    return noctopus.NMainWindow.singleton.proxySettings.connect(pyCallable)

def nConnectViewMode(pyCallable):
    return noctopus.NMainWindow.singleton.viewMode.connect(pyCallable)

def nConnectAppToggle(pyCallable):
    return noctopus.NSelector.singleton.appButtonToggle.connect(pyCallable)

def nConnectAppSelect(pyCallable):
    return noctopus.NSelector.singleton.appButtonPressed.connect(pyCallable)

def nSetStatusMsg(msg):
    return noctopus.NMainWindow.singleton.setStatusMsg(msg)
