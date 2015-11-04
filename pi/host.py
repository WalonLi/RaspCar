#!/usr/bin/python3

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

import sys
import socket
import time
from Motor import Motor


class RaspCar():
    def __init__(self):
        self._motor = Motor()
        #self._motor.turnRight()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('', 50007))
        self._socket.listen(1)
        pass

    def __del__(self):
        self._socket.close()

    def start(self):
        while True:
            conn, addr = self._socket.accept()
            print("Connected by", addr)
            while True:
                try:
                    # receive data
                    data = conn.recv(1024)

                    # force quit...
                    if data == "close":
                        return True

                    self._parseData(data)
                    #send feedback
                    conn.send("good")
                except:
                    print("close socket")
                    break
            conn.close()

    def _parseData(self, data):
        func = data.split(" ")
        if len(func) < 2:
            return

        key = func[0].split(":")
        act = func[1].split(":")
        if key[0] == "arrow-key" and act[0] == "action" :
            if act[1] == "press":
                if key[1] == "up":
                    self._motor.forward()
                elif key[1] == "mid-left":
                    self._motor.turnLeft()
                elif key[1] == "mid-right":
                    self._motor.turnRight()
                elif key[1] == "down":
                    self._motor.backward()
            elif act[1] == "release":
                self._motor.stop()
        #print(key, act)


if __name__ == '__main__' :
    car = RaspCar()
    car.start()
    print("hello")