from PySide import QtGui
from PySide import QtSvg
import os
import sys

def get(iconSet):
    return TkorderIcons.get(iconSet)

def getImage(imageSet):
    return TkorderImages.get(imageSet)

class TkorderIcons(object):
    @classmethod
    def init(cls):
        currentPath = os.path.dirname(sys.executable)
        iconsPath   = os.path.join(currentPath, 'icons')
        cls.iconSet = {
            'edit-redo': QtGui.QIcon(os.path.join(iconsPath, "edit-redo.svg")),
            'edit-undo': QtGui.QIcon(os.path.join(iconsPath, "edit-undo.svg")),
            'list-add': QtGui.QIcon(os.path.join(iconsPath, "list-add.svg")),
            'go-next': QtGui.QIcon(os.path.join(iconsPath, "go-next.svg")),
            'go-previous': QtGui.QIcon(os.path.join(iconsPath, "go-previous.svg")),
            'go-first': QtGui.QIcon(os.path.join(iconsPath, "go-first.svg")),
            'go-last': QtGui.QIcon(os.path.join(iconsPath, "go-last.svg")),
            'document-save-as': QtGui.QIcon(os.path.join(iconsPath, "document-save-as.svg")),
            'system-log-out': QtGui.QIcon(os.path.join(iconsPath, "system-log-out.svg")),
            'applications-development': QtGui.QIcon(os.path.join(iconsPath, "applications-development.svg")),
            'applications-multimedia': QtGui.QIcon(os.path.join(iconsPath, "applications-multimedia.svg")),
            'applications-system': QtGui.QIcon(os.path.join(iconsPath, "applications-system.svg")),
            'computer': QtGui.QIcon(os.path.join(iconsPath, "computer.svg")),
            'dialog-error': QtGui.QIcon(os.path.join(iconsPath, "dialog-error.svg")),
            'dialog-information': QtGui.QIcon(os.path.join(iconsPath, "dialog-information.svg")),
            'dialog-warning': QtGui.QIcon(os.path.join(iconsPath, "dialog-warning.svg")),
            'drive-harddisk': QtGui.QIcon(os.path.join(iconsPath, "drive-harddisk.svg")),
            'edit-clear': QtGui.QIcon(os.path.join(iconsPath, "edit-clear.svg")),
            'emblem-important': QtGui.QIcon(os.path.join(iconsPath, "emblem-important.svg")),
            'emblem-readonly': QtGui.QIcon(os.path.join(iconsPath, "emblem-readonly.svg")),
            'emblem-system': QtGui.QIcon(os.path.join(iconsPath, "emblem-system.svg")),
            'emblem-unreadable': QtGui.QIcon(os.path.join(iconsPath, "emblem-unreadable.svg")),
            'help-browser': QtGui.QIcon(os.path.join(iconsPath, "help-browser.svg")),
            'internet-news-reader': QtGui.QIcon(os.path.join(iconsPath, "internet-news-reader.svg")),
            'mail-attachment': QtGui.QIcon(os.path.join(iconsPath, "mail-attachment.svg")),
            'media-floppy': QtGui.QIcon(os.path.join(iconsPath, "media-floppy.svg")),
            'network-server': QtGui.QIcon(os.path.join(iconsPath, "network-server.svg")),
            'network-wired': QtGui.QIcon(os.path.join(iconsPath, "network-wired.svg")),
            'network-wireless': QtGui.QIcon(os.path.join(iconsPath, "network-wireless.svg")),
            'network-workgroup': QtGui.QIcon(os.path.join(iconsPath, "network-workgroup.svg")),
            'preferences-desktop-keyboard-shortcuts': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-keyboard-shortcuts.svg")),
            'preferences-desktop-locale': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-locale.svg")),
            'preferences-desktop-peripherals': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-peripherals.svg")),
            'preferences-desktop-screensaver': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-screensaver.svg")),
            'preferences-desktop': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop.svg")),
            'preferences-desktop-theme': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-theme.svg")),
            'preferences-desktop-wallpaper': QtGui.QIcon(os.path.join(iconsPath, "preferences-desktop-wallpaper.svg")),
            'preferences-system-session': QtGui.QIcon(os.path.join(iconsPath, "preferences-system-session.svg")),
            'preferences-system': QtGui.QIcon(os.path.join(iconsPath, "preferences-system.svg")),
            'start-here': QtGui.QIcon(os.path.join(iconsPath, "start-here.svg")),
            'system-installer': QtGui.QIcon(os.path.join(iconsPath, "system-installer.svg")),
            'system-log-out': QtGui.QIcon(os.path.join(iconsPath, "system-log-out.svg")),
            'system-shutdown': QtGui.QIcon(os.path.join(iconsPath, "system-shutdown.svg")),
            'utilities-system-monitor': QtGui.QIcon(os.path.join(iconsPath, "utilities-system-monitor.svg")),
            'utilities-system-monitor-black': QtGui.QIcon(os.path.join(iconsPath, "utilities-system-monitor-black.svg")),
            'utilities-terminal': QtGui.QIcon(os.path.join(iconsPath, "utilities-terminal.svg")),
            'process-stop': QtGui.QIcon(os.path.join(iconsPath, "process-stop.svg")),
            'video-display': QtGui.QIcon(os.path.join(iconsPath, "video-display.svg")),
            'weather-clear-night': QtGui.QIcon(os.path.join(iconsPath, "weather-clear-night.svg")),
            'weather-clear': QtGui.QIcon(os.path.join(iconsPath, "weather-clear.svg")),
            'weather-few-clouds-night': QtGui.QIcon(os.path.join(iconsPath, "weather-few-clouds-night.svg")),
            'weather-few-clouds': QtGui.QIcon(os.path.join(iconsPath, "weather-few-clouds.svg")),
            'weather-overcast': QtGui.QIcon(os.path.join(iconsPath, "weather-overcast.svg")),
            'weather-severe-alert': QtGui.QIcon(os.path.join(iconsPath, "weather-severe-alert.svg")),
            'weather-showers-scattered': QtGui.QIcon(os.path.join(iconsPath, "weather-showers-scattered.svg")),
            'weather-showers': QtGui.QIcon(os.path.join(iconsPath, "weather-showers.svg")),
            'weather-snow': QtGui.QIcon(os.path.join(iconsPath, "weather-snow.svg")),
            'weather-storm': QtGui.QIcon(os.path.join(iconsPath, "weather-storm.svg")),
            'Filter': QtGui.QIcon(os.path.join(iconsPath, "Filter.svg"))
        }

    @classmethod
    def get(cls, iconName):
        return cls.iconSet[iconName]

class TkorderImages(object):
    @classmethod
    def init(cls):
        currentPath = os.path.dirname(sys.executable)
        imagesPath  = os.path.join(currentPath, 'icons')
        cls.imageSet = {
            '60-day-trial-banner': os.path.join(imagesPath, "60-day-trial-banner.svg"),
            '60-day-trial-banner-reversed': os.path.join(imagesPath, "60-day-trial-banner-reversed.svg"),
            '30-day-trial-banner': os.path.join(imagesPath, "30-day-trial-banner.svg"),
            '30-day-trial-banner-reversed': os.path.join(imagesPath, "30-day-trial-banner-reversed.svg"),
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
            'Filter': os.path.join(imagesPath, "Filter.svg")
        }

    @classmethod
    def get(cls, iconName):
        return cls.imageSet[iconName]
