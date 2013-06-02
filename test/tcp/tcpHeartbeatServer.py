#!/usr/bin/env python2


import SocketServer
import time

class MyHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        err = None
        while (err == None):
            try: 
                err = self.request.sendall('hello')
                time.sleep(1)
            except ValueError:
                print "ok disco"
        
print "listening on port 8889 on localhost"
server = SocketServer.TCPServer(('localhost', 8889), MyHandler)
server.serve_forever()
