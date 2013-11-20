from PySide import QtGui
from PySide import QtSvg


def get(iconSet):
    return TkorderIcons.get(iconSet)

def getImage(imageSet):
    return TkorderImages.get(imageSet)

class TkorderIcons(object):
    @classmethod
    def init(cls):
        cls.iconSet = {
            'system-log-out': QtGui.QIcon("icons/system-log-out.svg"),
            'applications-development': QtGui.QIcon("icons/applications-development.svg"),
            'applications-multimedia': QtGui.QIcon("icons/applications-multimedia.svg"),
            'applications-system': QtGui.QIcon("icons/applications-system.svg"),
            'computer': QtGui.QIcon("icons/computer.svg"),
            'dialog-error': QtGui.QIcon("icons/dialog-error.svg"),
            'dialog-information': QtGui.QIcon("icons/dialog-information.svg"),
            'dialog-warning': QtGui.QIcon("icons/dialog-warning.svg"),
            'drive-harddisk': QtGui.QIcon("icons/drive-harddisk.svg"),
            'edit-clear': QtGui.QIcon("icons/edit-clear.svg"),
            'emblem-important': QtGui.QIcon("icons/emblem-important.svg"),
            'emblem-readonly': QtGui.QIcon("icons/emblem-readonly.svg"),
            'emblem-system': QtGui.QIcon("icons/emblem-system.svg"),
            'emblem-unreadable': QtGui.QIcon("icons/emblem-unreadable.svg"),
            'help-browser': QtGui.QIcon("icons/help-browser.svg"),
            'internet-news-reader': QtGui.QIcon("icons/internet-news-reader.svg"),
            'mail-attachment': QtGui.QIcon("icons/mail-attachment.svg"),
            'media-floppy': QtGui.QIcon("icons/media-floppy.svg"),
            'network-server': QtGui.QIcon("icons/network-server.svg"),
            'network-wired': QtGui.QIcon("icons/network-wired.svg"),
            'network-wireless': QtGui.QIcon("icons/network-wireless.svg"),
            'network-workgroup': QtGui.QIcon("icons/network-workgroup.svg"),
            'preferences-desktop-keyboard-shortcuts': QtGui.QIcon("icons/preferences-desktop-keyboard-shortcuts.svg"),
            'preferences-desktop-locale': QtGui.QIcon("icons/preferences-desktop-locale.svg"),
            'preferences-desktop-peripherals': QtGui.QIcon("icons/preferences-desktop-peripherals.svg"),
            'preferences-desktop-screensaver': QtGui.QIcon("icons/preferences-desktop-screensaver.svg"),
            'preferences-desktop': QtGui.QIcon("icons/preferences-desktop.svg"),
            'preferences-desktop-theme': QtGui.QIcon("icons/preferences-desktop-theme.svg"),
            'preferences-desktop-wallpaper': QtGui.QIcon("icons/preferences-desktop-wallpaper.svg"),
            'preferences-system-session': QtGui.QIcon("icons/preferences-system-session.svg"),
            'preferences-system': QtGui.QIcon("icons/preferences-system.svg"),
            'start-here': QtGui.QIcon("icons/start-here.svg"),
            'system-installer': QtGui.QIcon("icons/system-installer.svg"),
            'system-log-out': QtGui.QIcon("icons/system-log-out.svg"),
            'system-shutdown': QtGui.QIcon("icons/system-shutdown.svg"),
            'utilities-system-monitor': QtGui.QIcon("icons/utilities-system-monitor.svg"),
            'utilities-terminal': QtGui.QIcon("icons/utilities-terminal.svg"),
            'video-display': QtGui.QIcon("icons/video-display.svg"),
            'weather-clear-night': QtGui.QIcon("icons/weather-clear-night.svg"),
            'weather-clear': QtGui.QIcon("icons/weather-clear.svg"),
            'weather-few-clouds-night': QtGui.QIcon("icons/weather-few-clouds-night.svg"),
            'weather-few-clouds': QtGui.QIcon("icons/weather-few-clouds.svg"),
            'weather-overcast': QtGui.QIcon("icons/weather-overcast.svg"),
            'weather-severe-alert': QtGui.QIcon("icons/weather-severe-alert.svg"),
            'weather-showers-scattered': QtGui.QIcon("icons/weather-showers-scattered.svg"),
            'weather-showers': QtGui.QIcon("icons/weather-showers.svg"),
            'weather-snow': QtGui.QIcon("icons/weather-snow.svg"),
            'weather-storm': QtGui.QIcon("icons/weather-storm.svg"),
            'Filter': QtGui.QIcon("icons/Filter.svg")
        }

    @classmethod
    def get(cls, iconName):
        return cls.iconSet[iconName]

class TkorderImages(object):
    @classmethod
    def init(cls):
        cls.imageSet = {
            'system-log-out': "icons/system-log-out.svg",
            'applications-development': "icons/applications-development.svg",
            'applications-multimedia': "icons/applications-multimedia.svg",
            'applications-system': "icons/applications-system.svg",
            'computer': "icons/computer.svg",
            'dialog-error': "icons/dialog-error.svg",
            'dialog-information': "icons/dialog-information.svg",
            'dialog-warning': "icons/dialog-warning.svg",
            'drive-harddisk': "icons/drive-harddisk.svg",
            'edit-clear': "icons/edit-clear.svg",
            'emblem-important': "icons/emblem-important.svg",
            'emblem-readonly': "icons/emblem-readonly.svg",
            'emblem-system': "icons/emblem-system.svg",
            'emblem-unreadable': "icons/emblem-unreadable.svg",
            'help-browser': "icons/help-browser.svg",
            'internet-news-reader': "icons/internet-news-reader.svg",
            'mail-attachment': "icons/mail-attachment.svg",
            'media-floppy': "icons/media-floppy.svg",
            'network-server': "icons/network-server.svg",
            'network-wired': "icons/network-wired.svg",
            'network-wireless': "icons/network-wireless.svg",
            'network-workgroup': "icons/network-workgroup.svg",
            'preferences-desktop-keyboard-shortcuts': "icons/preferences-desktop-keyboard-shortcuts.svg",
            'preferences-desktop-locale': "icons/preferences-desktop-locale.svg",
            'preferences-desktop-peripherals': "icons/preferences-desktop-peripherals.svg",
            'preferences-desktop-screensaver': "icons/preferences-desktop-screensaver.svg",
            'preferences-desktop': "icons/preferences-desktop.svg",
            'preferences-desktop-theme': "icons/preferences-desktop-theme.svg",
            'preferences-desktop-wallpaper': "icons/preferences-desktop-wallpaper.svg",
            'preferences-system-session': "icons/preferences-system-session.svg",
            'preferences-system': "icons/preferences-system.svg",
            'start-here': "icons/start-here.svg",
            'system-installer': "icons/system-installer.svg",
            'system-log-out': "icons/system-log-out.svg",
            'system-shutdown': "icons/system-shutdown.svg",
            'utilities-system-monitor': "icons/utilities-system-monitor.svg",
            'utilities-terminal': "icons/utilities-terminal.svg",
            'video-display': "icons/video-display.svg",
            'weather-clear-night': "icons/weather-clear-night.svg",
            'weather-clear': "icons/weather-clear.svg",
            'weather-few-clouds-night': "icons/weather-few-clouds-night.svg",
            'weather-few-clouds': "icons/weather-few-clouds.svg",
            'weather-overcast': "icons/weather-overcast.svg",
            'weather-severe-alert': "icons/weather-severe-alert.svg",
            'weather-showers-scattered': "icons/weather-showers-scattered.svg",
            'weather-showers': "icons/weather-showers.svg",
            'weather-snow': "icons/weather-snow.svg",
            'weather-storm': "icons/weather-storm.svg",
            'Filter': "icons/Filter.svg"
        }

    @classmethod
    def get(cls, iconName):
        return cls.imageSet[iconName]
