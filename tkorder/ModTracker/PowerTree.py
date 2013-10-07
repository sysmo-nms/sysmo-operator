from    PySide import QtGui, QtCore
import  TkorderIcons
import  TrackerMain


def handle(msg):
    print "message :", msg

class Target(object):
    def __init_(self):
        print "create target"

class Probe(object):
    def __init__(self):
        print "create probe"

class PowerTreeContainer(QtGui.QFrame):
    @classmethod
    def setSingleton(cls, obj):
        cls.singleton = obj

    @classmethod
    def singleton(cls):
        return cls.singleton

    @classmethod
    def toggle(cls):
        if (cls.singleton.isHidden() == True):
            cls.singleton.show()
        else:
            cls.singleton.hide()


    def __init__(self, parent):
        super(PowerTreeContainer, self).__init__(parent)
        PowerTreeContainer.setSingleton(self)
