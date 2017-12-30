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

server_port = random.randint(10000, 11000)

def new_client(client, server):
    while (True):
        msg = '{"msg": "hi"}'
        server.send_message(client, msg)
        print msg + "\n"
        time.sleep(2)

def server():
    server = WebsocketServer(server_port)
    server.set_fn_new_client(new_client)
    server.run_forever()

def viewer():
    app = QApplication(sys.argv)
    pwd = os.getcwd();

    view = QWebView()
    view.setWindowFlags(Qt.FramelessWindowHint)

    f = open("tail.html", "r")
    html = f.read()
    html = html.replace("__PORT__", str(server_port))
    
    #view.load(QUrl("file://" + pwd + "/tail.html"))
    view.setHtml(html)
    view.show()

    app.exec_()

tail_thread = threading.Thread(target=server)
tail_thread.start()

viewer_thread = threading.Thread(target=viewer)
viewer_thread.start()

tail_thread.join()
viewer_thread.join()
