#!/usr/bin/python

import  sys
import  zlib
from    functools import partial
from    PySide.QtCore import (
    Qt,
    QUrl,
    QObject,
    QThread,
    Signal
)

from    PySide.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply
)

from PySide.QtGui import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton
)


def requestUrl(request):
    SupercastAccessManager.singleton.requestUrl(request)

class SupercastHTTPRequest(QNetworkRequest):
    def __init__(self, url):
        super(SupercastHTTPRequest, self).__init__(url)
        self.setAttribute(QNetworkRequest.HttpPipeliningAllowedAttribute, True)
        self.setRawHeader("Accept-Encoding", "deflate, gzip")


class SupercastAccessManagerThread(QObject):
    upSignal   = Signal(dict)
    def __init__(self, server, proto, port):
        super(SupercastAccessManagerThread, self).__init__(None)
        self._urlHead = "%s://%s:%i" % (proto, server, port)
        self._manager = QNetworkAccessManager(self)
        self._manager.finished[QNetworkReply].connect(self._handleReply)
        self._replyDict = dict()

    def _handleReply(self, reply):
        originalRequest = self._replyDict[reply]
        del self._replyDict[reply]
        uFile = open(originalRequest['outfile'], 'w+')
        uFile.write(zlib.decompress(reply.readAll(), 16+zlib.MAX_WBITS))
        uFile.close()
        reply.deleteLater()
        originalRequest['success'] = True
        self.upSignal.emit(originalRequest)

    def handleRequest(self, request):
        url     = request['url']
        fullPath = "%s/%s" % (self._urlHead, url)
        reply   = self._manager.get(SupercastHTTPRequest(QUrl(fullPath)))
        self._replyDict[reply] = request


class SupercastAccessManager(QObject):
    downSignal = Signal(dict)
    def __init__(self, parent, server, proto, dataPort):
        super(SupercastAccessManager, self).__init__(parent)
        SupercastAccessManager.singleton = self
        thread = QThread(self)
        self._managerDown = SupercastAccessManagerThread(server, proto, dataPort)
        self._managerDown.moveToThread(thread)
        thread.start()
        self.destroyed.connect(self._managerDown.deleteLater)
        self.destroyed.connect(thread.deleteLater)
        self._managerDown.upSignal.connect(self._handleReply, Qt.QueuedConnection)
        self.downSignal.connect(self._managerDown.handleRequest, Qt.QueuedConnection)

    def _handleReply(self, reply):
        callback = reply['callback']
        callback(reply)

    def requestUrl(self, request):
        "when request is a dict {'url': url, 'outfile': file, callback: callback}"
        self.downSignal.emit(request)


class SupercastHTTPTest(QWidget):
    def __init__(self, parent=None):
        super(SupercastHTTPTest, self).__init__(parent)
        self.manager = SupercastAccessManager(self)
        self._url = QUrl("http://localhost:8080/tmp-390146165879/1.xml")

    def buttonPushed(self):
        request = dict()
        request['url']      = self._url
        request['outfile']  = 'jojo.rrd'
        request['callback'] = self._handleReply
        reply1 = self.manager.requestUrl(request)

    def _handleReply(self, reply):
        print "end reply", reply

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wid = SupercastHTTPTest()
    wid.resize(250, 150)
    wid.setWindowTitle('Simple')
    grid = QGridLayout(wid)
    but = QPushButton('Exec', wid)
    but.pressed.connect(wid.buttonPushed)
    grid.addWidget(but)
    wid.setLayout(grid)
    wid.show()
    sys.exit(app.exec_())
