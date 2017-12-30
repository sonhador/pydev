import os
import sys
import time
import random
import logging
import threading
from websocket_server import WebsocketServer
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class ClientServer:
    browser = None
    server_port = None
    server = None

    def __init__(self):
        self.server_port = random.randint(10000, 11000)
        self.server = WebsocketServer(self.server_port)
    
        server_thread = threading.Thread(target=self.websocket_server)
        server_thread.start()

        viewer_thread = threading.Thread(target=self.websocket_viewer)
        viewer_thread.start()

    def websocket_client(self, client, server):
        cnt = 0
        while (cnt < 3):
            msg = '{"msg": "hi"}'
            self.server.send_message(client, msg)
            print msg + "\n"
            time.sleep(2)
            cnt += 1

        self.server.server_close()
        self.browser.exit()

    def websocket_server(self):
        self.server.set_fn_new_client(self.websocket_client)
        self.server.run_forever()

    def websocket_viewer(self):
        self.browser = QApplication(sys.argv)
        view = QWebView()
        view.setWindowFlags(Qt.FramelessWindowHint)

        f = open("tail.html", "r")
        html = f.read()
        html = html.replace("__PORT__", str(self.server_port))
        
        # pwd = os.getcwd();
        # view.load(QUrl("file://" + pwd + "/tail.html"))
        view.setHtml(html)
        view.show()

        self.browser.exec_()

ClientServer()
