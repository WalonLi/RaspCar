
"""
GNU GENERAL PUBLIC LICENSE
Copyright (C) 2015  WalonLi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
