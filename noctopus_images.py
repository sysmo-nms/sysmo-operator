import  os, sys, platform
from    PyQt5.QtWidgets import (
    QWidget
)
from    PyQt5.QtGui import (
    QIcon,
    QPalette,
    QPixmap
)

iconPixSet  = dict()
pixmapSet   = dict()
iconSet     = dict()
imageSet    = dict()
hexRgbSet   = dict()
hexRgbaSet  = dict()

if platform.system() == 'Windows':
    currentPath = os.path.dirname(sys.executable)
else:
    currentPath = os.path.dirname(__file__)
iconsPath   = os.path.join(currentPath, 'graphics')
imagesPath  = os.path.join(currentPath, 'graphics')

def noctopusGraphicsInit():
    initIcons()
    initImages()
    initHexSet()

def getPixmap(name):
    if name in pixmapSet: return pixmapSet[name]
    global iconsPath
    filename = "%s.png" % name
    filepath = os.path.join(iconsPath, filename)
    pixmapSet[name] = QPixmap(filepath)
    return pixmapSet[name]
    
def getIcon(icon):
    global iconSet
    return iconSet[icon]

def getImage(image):
    global imageSet
    return imageSet[image]

def getRgb(pal):
    global hexRgbSet
    return hexRgbSet[pal]

def getRgba(pal):
    global hexRgbaSet
    return hexRgbaSet[pal]

def initIcons():
    global iconsPath
    global iconSet
    iconSet = {

        'satellite': QIcon(os.path.join(iconsPath, "satellite.svg")),
        'printer': QIcon(os.path.join(iconsPath, "printer.svg")),
        'server': QIcon(os.path.join(iconsPath, "server.svg")),
        'firewall': QIcon(os.path.join(iconsPath, "firewall.svg")),
        'switch': QIcon(os.path.join(iconsPath, "switch.svg")),
        'router': QIcon(os.path.join(iconsPath, "router.svg")),
        'wireless': QIcon(os.path.join(iconsPath, "wireless.svg")),
        'document-save': QIcon(os.path.join(iconsPath, "document-save.svg")),
        'accessories-text-editor': QIcon(os.path.join(iconsPath, "accessories-text-editor.svg")),
        'edit-paste': QIcon(os.path.join(iconsPath, "edit-paste.svg")),
        'media-playback-pause': QIcon(os.path.join(iconsPath, "media-playback-pause.svg")),
        'text-x-generic-template': QIcon(os.path.join(iconsPath, "text-x-generic-template.svg")),
        'face-devilish': QIcon(os.path.join(iconsPath, "face-devilish.svg")),
        'face-smile': QIcon(os.path.join(iconsPath, "face-smile.svg")),
        'software-update-available': QIcon(os.path.join(iconsPath, "software-update-available.svg")),
        'software-update-urgent': QIcon(os.path.join(iconsPath, "software-update-urgent.svg")),
        'system-users': QIcon(os.path.join(iconsPath, "system-users.svg")),
        'preferences-system-windows': QIcon(os.path.join(iconsPath, "preferences-system-windows.svg")),
        'appointment-new': QIcon(os.path.join(iconsPath, "appointment-new.svg")),
        'system-search': QIcon(os.path.join(iconsPath, "system-search.svg")),
        'x-office-drawing': QIcon(os.path.join(iconsPath, "x-office-drawing.svg")),
        'internet-web-browser': QIcon(os.path.join(iconsPath, "internet-web-browser.svg")),
        'folder-saved-search': QIcon(os.path.join(iconsPath, "folder-saved-search.svg")),
        'list-remove': QIcon(os.path.join(iconsPath, "list-remove.svg")),
        'go-up': QIcon(os.path.join(iconsPath, "go-up.svg")),
        'go-down': QIcon(os.path.join(iconsPath, "go-down.svg")),
        'edit-redo': QIcon(os.path.join(iconsPath, "edit-redo.svg")),
        'edit-undo': QIcon(os.path.join(iconsPath, "edit-undo.svg")),
        'list-add': QIcon(os.path.join(iconsPath, "list-add.svg")),
        'go-next': QIcon(os.path.join(iconsPath, "go-next.svg")),
        'go-previous': QIcon(os.path.join(iconsPath, "go-previous.svg")),
        'go-first': QIcon(os.path.join(iconsPath, "go-first.svg")),
        'go-last': QIcon(os.path.join(iconsPath, "go-last.svg")),
        'document-save-as': QIcon(os.path.join(iconsPath, "document-save-as.svg")),
        'system-log-out': QIcon(os.path.join(iconsPath, "system-log-out.svg")),
        'applications-development': QIcon(os.path.join(iconsPath, "applications-development.svg")),
        'applications-multimedia': QIcon(os.path.join(iconsPath, "applications-multimedia.svg")),
        'applications-system': QIcon(os.path.join(iconsPath, "applications-system.svg")),
        'computer': QIcon(os.path.join(iconsPath, "computer.svg")),
        'dialog-error': QIcon(os.path.join(iconsPath, "dialog-error.svg")),
        'dialog-information': QIcon(os.path.join(iconsPath, "dialog-information.svg")),
        'dialog-warning': QIcon(os.path.join(iconsPath, "dialog-warning.svg")),
        'drive-harddisk': QIcon(os.path.join(iconsPath, "drive-harddisk.svg")),
        'edit-clear': QIcon(os.path.join(iconsPath, "edit-clear.svg")),
        'emblem-important': QIcon(os.path.join(iconsPath, "emblem-important.svg")),
        'emblem-readonly': QIcon(os.path.join(iconsPath, "emblem-readonly.svg")),
        'emblem-system': QIcon(os.path.join(iconsPath, "emblem-system.svg")),
        'emblem-unreadable': QIcon(os.path.join(iconsPath, "emblem-unreadable.svg")),
        'help-browser': QIcon(os.path.join(iconsPath, "help-browser.svg")),
        'internet-news-reader': QIcon(os.path.join(iconsPath, "internet-news-reader.svg")),
        'mail-attachment': QIcon(os.path.join(iconsPath, "mail-attachment.svg")),
        'media-floppy': QIcon(os.path.join(iconsPath, "media-floppy.svg")),
        'network-server': QIcon(os.path.join(iconsPath, "network-server.svg")),
        'network-wired': QIcon(os.path.join(iconsPath, "network-wired.svg")),
        'network-wireless': QIcon(os.path.join(iconsPath, "network-wireless.svg")),
        'network-workgroup': QIcon(os.path.join(iconsPath, "network-workgroup.svg")),
        'preferences-desktop-keyboard-shortcuts': QIcon(os.path.join(iconsPath, "preferences-desktop-keyboard-shortcuts.svg")),
        'preferences-desktop-locale': QIcon(os.path.join(iconsPath, "preferences-desktop-locale.svg")),
        'preferences-desktop-peripherals': QIcon(os.path.join(iconsPath, "preferences-desktop-peripherals.svg")),
        'preferences-desktop-screensaver': QIcon(os.path.join(iconsPath, "preferences-desktop-screensaver.svg")),
        'preferences-desktop': QIcon(os.path.join(iconsPath, "preferences-desktop.svg")),
        'preferences-desktop-theme': QIcon(os.path.join(iconsPath, "preferences-desktop-theme.svg")),
        'preferences-desktop-wallpaper': QIcon(os.path.join(iconsPath, "preferences-desktop-wallpaper.svg")),
        'preferences-system-session': QIcon(os.path.join(iconsPath, "preferences-system-session.svg")),
        'preferences-system': QIcon(os.path.join(iconsPath, "preferences-system.svg")),
        'start-here': QIcon(os.path.join(iconsPath, "start-here.svg")),
        'system-installer': QIcon(os.path.join(iconsPath, "system-installer.svg")),
        'system-log-out': QIcon(os.path.join(iconsPath, "system-log-out.svg")),
        'system-shutdown': QIcon(os.path.join(iconsPath, "system-shutdown.svg")),
        'utilities-system-monitor': QIcon(os.path.join(iconsPath, "utilities-system-monitor.svg")),
        'monitor-black': QIcon(os.path.join(iconsPath, "monitor-black.svg")),
        'monitor-white': QIcon(os.path.join(iconsPath, "monitor-white.svg")),
        'dashboard-black': QIcon(os.path.join(iconsPath, "dashboard-black.svg")),
        'netman-black': QIcon(os.path.join(iconsPath, "netman-black.svg")),
        'netman-white': QIcon(os.path.join(iconsPath, "netman-white.svg")),
        'iphelper-black': QIcon(os.path.join(iconsPath, "iphelper-black.svg")),
        'iphelper-white': QIcon(os.path.join(iconsPath, "iphelper-white.svg")),
        'knowledge-black': QIcon(os.path.join(iconsPath, "knowledge-black.svg")),
        'knowledge-white': QIcon(os.path.join(iconsPath, "knowledge-white.svg")),
        'utilities-terminal': QIcon(os.path.join(iconsPath, "utilities-terminal.svg")),
        'process-stop': QIcon(os.path.join(iconsPath, "process-stop.svg")),
        'video-display': QIcon(os.path.join(iconsPath, "video-display.svg")),
        'weather-clear-night': QIcon(os.path.join(iconsPath, "weather-clear-night.svg")),
        'weather-clear': QIcon(os.path.join(iconsPath, "weather-clear.svg")),
        'weather-few-clouds-night': QIcon(os.path.join(iconsPath, "weather-few-clouds-night.svg")),
        'weather-few-clouds': QIcon(os.path.join(iconsPath, "weather-few-clouds.svg")),
        'weather-overcast': QIcon(os.path.join(iconsPath, "weather-overcast.svg")),
        'weather-severe-alert': QIcon(os.path.join(iconsPath, "weather-severe-alert.svg")),
        'weather-showers-scattered': QIcon(os.path.join(iconsPath, "weather-showers-scattered.svg")),
        'weather-showers': QIcon(os.path.join(iconsPath, "weather-showers.svg")),
        'weather-snow': QIcon(os.path.join(iconsPath, "weather-snow.svg")),
        'weather-storm': QIcon(os.path.join(iconsPath, "weather-storm.svg")),
        'Filter': QIcon(os.path.join(iconsPath, "Filter.svg"))
    }
    
# IMAGES
def initImages():
    global imageSet
    global imagesPath
    imageSet = {
        'document-save': os.path.join(imagesPath, "document-save.svg"),
        'accessories-text-editor': os.path.join(imagesPath, "accessories-text-editor.svg"),
        'edit-paste': os.path.join(imagesPath, "edit-paste.svg"),
        'media-playback-pause': os.path.join(imagesPath, "media-playback-pause.svg"),
        'media-playback-start': os.path.join(imagesPath, "media-playback-start.svg"),
        'rrdtool-logo': os.path.join(imagesPath, "rrdtool_logo.png"),
        '60-day-trial-banner': os.path.join(imagesPath, "60-day-trial-banner.svg"),
        '60-day-trial-banner-reversed': os.path.join(imagesPath, "60-day-trial-banner-reversed.svg"),
        '30-day-trial-banner': os.path.join(imagesPath, "30-day-trial-banner.svg"),
        '30-day-trial-banner-reversed': os.path.join(imagesPath, "30-day-trial-banner-reversed.svg"),
        'face-devilish': os.path.join(imagesPath, "face-devilish.svg"),
        'face-smile': os.path.join(imagesPath, "face-smile.svg"),
        'software-update-available': os.path.join(imagesPath, "software-update-available.svg"),
        'software-update-urgent': os.path.join(imagesPath, "software-update-urgent.svg"),
        'system-users': os.path.join(imagesPath, "system-users.svg"),
        'preferences-system-windows': os.path.join(imagesPath, "preferences-system-windows.svg"),
        'system-search': os.path.join(imagesPath, "system-search.svg"),
        'appointment-new': os.path.join(imagesPath, "appointment-new.svg"),
        'internet-web-browser': os.path.join(imagesPath, "internet-web-browser.svg"),
        'folder-saved-search': os.path.join(imagesPath, "folder-saved-search.svg"),
        'list-remove': os.path.join(imagesPath, "list-remove.svg"),
        'go-up': os.path.join(imagesPath, "go-up.svg"),
        'go-down': os.path.join(imagesPath, "go-down.svg"),
        'edit-undo': os.path.join(imagesPath, "edit-undo.svg"),
        'edit-redo': os.path.join(imagesPath, "edit-redo.svg"),
        'list-add': os.path.join(imagesPath, "list-add.svg"),
        'system-log-out': os.path.join(imagesPath, "system-log-out.svg"),
        'applications-development': os.path.join(imagesPath, "applications-development.svg"),
        'applications-multimedia': os.path.join(imagesPath, "applications-multimedia.svg"),
        'applications-system': os.path.join(imagesPath, "applications-system.svg"),
        'computer': os.path.join(imagesPath, "computer.svg"),
        'dialog-error': os.path.join(imagesPath, "dialog-error.svg"),
        'dialog-information': os.path.join(imagesPath, "dialog-information.svg"),
        'dialog-warning': os.path.join(imagesPath, "dialog-warning.svg"),
        'drive-harddisk': os.path.join(imagesPath, "drive-harddisk.svg"),
        'edit-clear': os.path.join(imagesPath, "edit-clear.svg"),
        'emblem-important': os.path.join(imagesPath, "emblem-important.svg"),
        'emblem-readonly': os.path.join(imagesPath, "emblem-readonly.svg"),
        'emblem-system': os.path.join(imagesPath, "emblem-system.svg"),
        'emblem-unreadable': os.path.join(imagesPath, "emblem-unreadable.svg"),
        'help-browser': os.path.join(imagesPath, "help-browser.svg"),
        'internet-news-reader': os.path.join(imagesPath, "internet-news-reader.svg"),
        'mail-attachment': os.path.join(imagesPath, "mail-attachment.svg"),
        'media-floppy': os.path.join(imagesPath, "media-floppy.svg"),
        'network-server': os.path.join(imagesPath, "network-server.svg"),
        'network-wired': os.path.join(imagesPath, "network-wired.svg"),
        'network-wireless': os.path.join(imagesPath, "network-wireless.svg"),
        'network-workgroup': os.path.join(imagesPath, "network-workgroup.svg"),
        'preferences-desktop-keyboard-shortcuts': os.path.join(imagesPath, "preferences-desktop-keyboard-shortcuts.svg"),
        'preferences-desktop-locale': os.path.join(imagesPath, "preferences-desktop-locale.svg"),
        'preferences-desktop-peripherals': os.path.join(imagesPath, "preferences-desktop-peripherals.svg"),
        'preferences-desktop-screensaver': os.path.join(imagesPath, "preferences-desktop-screensaver.svg"),
        'preferences-desktop': os.path.join(imagesPath, "preferences-desktop.svg"),
        'preferences-desktop-theme': os.path.join(imagesPath, "preferences-desktop-theme.svg"),
        'preferences-desktop-wallpaper': os.path.join(imagesPath, "preferences-desktop-wallpaper.svg"),
        'preferences-system-session': os.path.join(imagesPath, "preferences-system-session.svg"),
        'preferences-system': os.path.join(imagesPath, "preferences-system.svg"),
        'start-here': os.path.join(imagesPath, "start-here.svg"),
        'system-installer': os.path.join(imagesPath, "system-installer.svg"),
        'system-log-out': os.path.join(imagesPath, "system-log-out.svg"),
        'system-shutdown': os.path.join(imagesPath, "system-shutdown.svg"),
        'utilities-system-monitor': os.path.join(imagesPath, "utilities-system-monitor.svg"),
        'utilities-terminal': os.path.join(imagesPath, "utilities-terminal.svg"),
        'video-display': os.path.join(imagesPath, "video-display.svg"),
        'weather-clear-night': os.path.join(imagesPath, "weather-clear-night.svg"),
        'weather-clear': os.path.join(imagesPath, "weather-clear.svg"),
        'weather-few-clouds-night': os.path.join(imagesPath, "weather-few-clouds-night.svg"),
        'weather-few-clouds': os.path.join(imagesPath, "weather-few-clouds.svg"),
        'weather-overcast': os.path.join(imagesPath, "weather-overcast.svg"),
        'weather-severe-alert': os.path.join(imagesPath, "weather-severe-alert.svg"),
        'weather-showers-scattered': os.path.join(imagesPath, "weather-showers-scattered.svg"),
        'weather-showers': os.path.join(imagesPath, "weather-showers.svg"),
        'weather-snow': os.path.join(imagesPath, "weather-snow.svg"),
        'weather-storm': os.path.join(imagesPath, "weather-storm.svg"),
        'Filter': os.path.join(imagesPath, "Filter.svg"),
        'monitor-black': os.path.join(imagesPath, "monitor-black.svg"),
        'monitor-white': os.path.join(imagesPath, "monitor-white.svg"),
        'dashboard-black': os.path.join(imagesPath, "dashboard-black.svg"),
        'netman-black': os.path.join(imagesPath, "netman-black.svg"),
        'netman-white': os.path.join(imagesPath, "netman-white.svg"),
        'iphelper-black': os.path.join(imagesPath, "iphelper-black.svg"),
        'iphelper-white': os.path.join(imagesPath, "iphelper-white.svg"),
        'knowledge-black': os.path.join(imagesPath, "knowledge-black.svg"),
        'knowledge-white': os.path.join(imagesPath, "knowledge-white.svg")
    }

def initHexSet():

    " For widgets who need hexadecimal version of the colors actualy used "
    " by the application (rrdtool)"

    global hexRgbaSet
    global hexRgbSet

    _wid = QWidget()
    pal  = _wid.palette()
    _wid.deleteLater()

    constDict = {
        'Window':       QPalette.Window,
        'WindowText':   QPalette.WindowText,
        'Base':         QPalette.Base,
        'AlternateBase':    QPalette.AlternateBase,
        'ToolTipBase':  QPalette.ToolTipBase,
        'ToolTipText':  QPalette.ToolTipText,
        'Text':         QPalette.Text,
        'Button':       QPalette.Button,
        'ButtonText':   QPalette.ButtonText,
        'BrightText':   QPalette.BrightText,
        'Light':        QPalette.Light,
        'MidLight':     QPalette.Midlight,
        'Dark':         QPalette.Dark,
        'Mid':          QPalette.Mid,
        'Shadow':       QPalette.Shadow
    }

    for key in list(constDict.keys()):
        col             = pal.color(constDict[key])
        (r,g,b,a)       = col.getRgb()
        hexRgbaSet[key] = "#%0.2X%0.2X%0.2X%0.2X" % (r,g,b,a)
        hexRgbSet[key]  = "#%0.2X%0.2X%0.2X" % (r,g,b)

def dumpPalette():
    _wid = QWidget()
    palette  = _wid.palette()
    _wid.deleteLater()

    colorGroups = dict()
    colorGroups['QPalette.Disabled'] = QPalette.Disabled
    colorGroups['QPalette.Active']   = QPalette.Active
    colorGroups['QPalette.Inactive'] = QPalette.Inactive
    colorGroups['QPalette.Normal']   = QPalette.Normal

    colorRoles = dict()
    colorRoles['QPalette.Window']       = QPalette.Window
    colorRoles['QPalette.Background']   = QPalette.Background
    colorRoles['QPalette.WindowText']   = QPalette.WindowText
    colorRoles['QPalette.Foreground']   = QPalette.Foreground
    colorRoles['QPalette.Base']         = QPalette.Base
    colorRoles['QPalette.AlternateBase'] = QPalette.AlternateBase
    colorRoles['QPalette.ToolTipBase']  = QPalette.ToolTipBase
    colorRoles['QPalette.ToolTipText']  = QPalette.ToolTipText
    colorRoles['QPalette.Text']         = QPalette.Text
    colorRoles['QPalette.Button']       = QPalette.Button
    colorRoles['QPalette.ButtonText']   = QPalette.ButtonText
    colorRoles['QPalette.BrightText']   = QPalette.BrightText
    colorRoles['QPalette.Light']        = QPalette.Light
    colorRoles['QPalette.Midlight']     = QPalette.Midlight
    colorRoles['QPalette.Dark']         = QPalette.Dark
    colorRoles['QPalette.Mid']          = QPalette.Mid
    colorRoles['QPalette.Shadow']       = QPalette.Shadow
    colorRoles['QPalette.Highlight']    = QPalette.Highlight
    colorRoles['QPalette.HighlightedText'] = QPalette.HighlightedText
    colorRoles['QPalette.Link']         = QPalette.Link
    colorRoles['QPalette.LinkVisited']  = QPalette.LinkVisited

    paletteDump = dict()
    for group in list(colorGroups.keys()):
        cGroup = colorGroups[group]
        paletteDump[cGroup] = dict()
        for role in list(colorRoles.keys()):
            cRole = colorRoles[role]
            color = palette.color(
                cGroup,
                cRole
            )
            rgb = color.getRgb()
            paletteDump[cGroup][cRole] = rgb

    f = open('palette.dump', 'w')
    f.write(str(paletteDump))
    f.close()
