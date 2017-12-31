import os
import sys
import time
import random
import socket
import tailer
import logging
import tempfile
import threading
from websocket_server import WebsocketServer
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class TailClientServer:
    browser = None
    server_port = None
    server = None
    filename = None
    fh = None

    def __init__(self, filename):
        while (True):
            self.server_port = random.randint(10000, 11000)
            if (self.port_available(self.server_port)):
                break

        self.filename = filename
        self.server = WebsocketServer(self.server_port)
    
        server_thread = threading.Thread(target=self.websocket_server)
        server_thread.start()

        viewer_thread = threading.Thread(target=self.websocket_viewer)
        viewer_thread.daemon = True
        viewer_thread.start()

    def port_available(self, port):
        print "Checking port " + str(port) + " for availability .. "

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = sock.connect_ex(('127.0.0.1', port))

        if (res == 0):
            print "Not Available\n"
            return False
        else:
            print "Available\n"
            return True

    def terminate(self):
        fh.close()
        self.browser.exit()
        self.server.shutdown()
        
    def websocket_client(self, client, server):
        print "Starting to tail.."

        fh = open(self.filename)

        for line in tailer.follow(fh):
            msg = '{"msg":"' + line + '"}'
            print msg
            self.server.send_message(client, msg)

    def websocket_server(self):
        self.server.set_fn_new_client(self.websocket_client)
        self.server.run_forever()

    def websocket_viewer(self):
        self.browser = QApplication(sys.argv)

        view = QWebView()
        view.setWindowFlags(Qt.FramelessWindowHint)
        view.setAttribute(Qt.WA_TranslucentBackground)
        view.setAttribute(Qt.WA_OpaquePaintEvent, False)

        page = view.page()
        palette = page.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        page.setPalette(palette)

        f = open("tail.html", "r")
        html = f.read()
        html = html.replace("__PORT__", str(self.server_port))
        
        # pwd = os.getcwd();
        # view.load(QUrl("file://" + pwd + "/tail.html"))
        view.setHtml(html)
        view.show()

        self.browser.exec_()

fh = tempfile.NamedTemporaryFile()
tailClientServer = TailClientServer(fh.name)

time.sleep(3)

cnt = 0
while (cnt < 5):
    fh.write("hi\n")
    fh.flush()
    print "hi"
    time.sleep(1)
    cnt += 1

tailClientServer.terminate()
fh.close()
