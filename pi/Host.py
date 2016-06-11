#!/usr/bin/python3

"""
author : Walon Li
"""

import sys
import socket
import time
from Motor import Motor


class RaspCar():
    def __init__(self):
        self._motor = Motor()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('', 50007))
        self._socket.listen(1)
        pass

    def __del__(self):
        self._socket.close()

    def start(self):
        print("start...")
        while True:
            conn, addr = self._socket.accept()
            print("Connected by", addr)
            while True:
                try:
                    # receive data
                    data = conn.recv(1024)
                    data = data.decode("utf-8")
                    # force quit...
                    if data == "close":
                        conn.close()
                        self._socket.close()
                        return True

                    self._parseData(data)

                    #send feedback
                    conn.send(bytes("good", "utf8"))
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
    print("car stop")