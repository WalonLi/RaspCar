
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

    def send_action(self, data):
        self.tcpSocket.send(bytes(data, "utf8"))
        rev_data = self.recv()
        print(rev_data)
        return True

    def recv(self):
        return self.tcpSocket.recv(1024)

    def close(self):
        self.tcpSocket.close()





'''
# host
# Echo server program
import socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        print('wait for message')
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
conn.close()


#client
# Echo client program
import socket
HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    a = input()
    s.send(b'Hello, world')
    data = s.recv(1024)
s.close()
print('Received', repr(data))
'''