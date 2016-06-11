
"""
author : Walon Li
"""

from PyQt5.QtNetwork import QUdpSocket, QTcpSocket
from PyQt5.QtCore import *
import socket

class ClientSocket():
    def __init__(self):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        try:
            self.tcpSocket.connect((host, port))
            return True
        except:
            print("get exception...")
            return False

    def sendAction(self, data):
        try:
            self.tcpSocket.send(bytes(data, "utf8"))

            # force close
            if data == "close" :
                return True

            rev_data = self.recv()
            while rev_data != b'good':
                rev_data = self.recv()
            print(rev_data)
            return True
        except:
            print("send action fail")
            return False

    def recv(self):
        try:
            return self.tcpSocket.recv(1024)
        except:
            return "Error recv"

    def close(self):
        self.tcpSocket.close()
