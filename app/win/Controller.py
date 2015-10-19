import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QHBoxLayout
import socket
from ClientSocket import ClientSocket
from PyQt5.uic import loadUi
from PyQt5.QtGui  import *
from PyQt5.QtCore import *
'''
class Enviroment:
    app = QApplication(sys.argv)
    def MoveToCenter(self, size):
        if app.desktop().screenCount() <= 1 :
            self.move((app.desktop().width()-size.width())/2, (app.desktop().height()-size.height())/2)
        else :
            rect = app.desktop().screenGeometry(0)
            self.move((rect.width()-self.width())/2, (rect.height()-self.height())/2)
            self.size()
'''

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__(None)

        # connet button
        self._btn = QPushButton("Connect")
        self._btn.setFixedSize(140, 30)
        self._btn.clicked.connect(self._connectPi)

        # ip text editor
        self._ipText = QTextEdit("localhost")
        self._ipText.setFixedSize(140, 30)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._ipText)
        self._layout.addWidget(self._btn)

        #
        self.setWindowTitle("RaspCar Windows Controller")
        self.setFixedSize(400, 200)
        self.setLayout(self._layout)


    def show(self):
        if app.desktop().screenCount() <= 1 :
            self.move((app.desktop().width()-self.width())/2, (app.desktop().height()-self.height())/2)
        else :
            rect = app.desktop().screenGeometry(0)
            self.move((rect.width()-self.width())/2, (rect.height()-self.height())/2)

        super().show()

    def _connectPi(self):
        print("connect Pi...", self._ipText.toPlainText())
        contol.bindSocket(self._ipText.toPlainText(), 50007)
        self.close()
        contol.show()





class ControlWindow(QWidget):

    def __init__(self):
        super().__init__(None)

        self._btn = QPushButton("Send")
        self._btn.clicked.connect(self.send_event)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._btn)

        self.setLayout(self._layout)
        self.setWindowTitle("RaspCar Windows Controller")
        self.setFixedSize(800, 600)

        self._sock = ClientSocket()


    def __del__(self):
        self._sock.close()

    def bindSocket(self, host, port):
        self._sock.connect(host, port)

    def send_event(self):
        while self._sock.send_action() == False:
            print("reconnect...")
#def init_login_layout() :
#    print("23")
#    print("23")




if __name__ == '__main__' :
    app = QApplication(sys.argv)

    login = LoginWindow()
    contol = ControlWindow()

    login.show()

    # a = QPushButton("Connect")
    # login.close()
    # app.exec_()

    sys.exit(app.exec_())
