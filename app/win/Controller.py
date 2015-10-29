import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QOpenGLWidget, QAction
import socket
from ClientSocket import ClientSocket
from PyQt5.uic import loadUi
from PyQt5.QtGui  import *
from PyQt5.QtCore import *


import time, threading

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

class BtnWidget(QPushButton):
    keyPressed = pyqtSignal()
    def keyPressEvent(self, event):
        print("fff..1")
        super(BtnWidget, self).keyPressEvent(event)
        print("fff..")
        self.keyPressed.emit()
'''


class TriggerObj(QObject):
    trigger = pyqtSignal()


class ConnectThread(threading.Thread):
    flag = False

    def run(self):
        #ConnectThread.connect_mutex.lock()
        print("connect Pi...", login._ipText.toPlainText())
        if control.bindSocket(login._ipText.toPlainText(), 50007):
            print("connect success...")
            obj = TriggerObj()
            obj.trigger.connect(login.changeView)
            obj.trigger.emit()
        else:
            print("connect fail...")

        ConnectThread.flag = False

    #def start(self, args):
    #    ConnectThread.args = args
    #    super().start()


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
        if not ConnectThread.flag:
            ConnectThread.flag = True
            ConnectThread().start()

    @pyqtSlot()
    def changeView(self):
        login.close()
        control.show()




class ControlWindow(QWidget):

    def __init__(self):
        super().__init__(None)

        self._up_left   = QPushButton("↖", self)
        self._up        = QPushButton("↑", self)
        self._up_right  = QPushButton("↗", self)
        self._mid_left  = QPushButton("←", self)
        self._mid       = QPushButton("", self)
        self._mid_right = QPushButton("→", self)
        self._down_left = QPushButton("↙", self)
        self._down      = QPushButton("↓", self)
        self._down_right = QPushButton("↘", self)

        btn_grp = [self._up_left, self._up, self._up_right,
                   self._mid_left, self._mid, self._mid_right,
                   self._down_left, self._down, self._down_right]
        press_event = [self.up_left_press_event, self.up_press_event, self.up_right_press_event,
                       self.mid_left_press_event, self.mid_press_event, self.mid_right_press_event,
                       self.down_left_press_event, self.down_press_event, self.down_right_press_event]
        release_event = [self.up_left_release_event, self.up_release_event, self.up_right_release_event,
                         self.mid_left_release_event, self.mid_release_event, self.mid_right_release_event,
                         self.down_left_release_event, self.down_release_event, self.down_right_release_event]

        # set position and connect event
        p = QPoint(620, 420) # start point
        for i in range(len(btn_grp)):
            btn_grp[i].setFixedSize(QSize(50, 50))
            btn_grp[i].move(p)
            btn_grp[i].pressed.connect(press_event[i])
            btn_grp[i].released.connect(release_event[i])
            if p.x() >= 740:
                p.setX(620)
                p.setY(p.y()+60)
            else:
                p.setX(p.x()+60)

        #act = QAction("Action", self._up_left, )
        self._up_left.setShortcut(Qt.Key_Left)
        #self._up_left.shor

        #self._up_left.addAction()
        #self._up.clicked.connect(self.send_event)

        self._graphic = QOpenGLWidget(self)
        self._graphic.setFixedSize(QSize(500, 400))
        self._graphic.move(QPoint(10, 10))


        #self._layout.set
        #self._layout = QGridLayout(self)
        #self._layout.addWidget(self._up)
        #self._layout.addWidget(self._down)

        #self.setLayout(self._layout)
        self.setWindowTitle("RaspCar Windows Controller")
        self.setFixedSize(800, 600)

        self._sock = ClientSocket()


    def __del__(self):
        self._sock.close()

    def bindSocket(self, host, port):
        return self._sock.connect(host, port)

    def send_event(self):
        while self._sock.send_action() == False:
            print("reconnect...")

    """
    def event(self, e):
        #if type(e) == QKeyEvent and not e.isAutoRepeat():
        #    if e.key() == Qt.Key_Up:
        #        print("123")
        #        return True

        #print(type(e))
        return QWidget.event(self, e)
    """

    #press function
    def up_left_press_event(self):
        print("up_left press")
        pass
    def up_press_event(self):
        pass
    def up_right_press_event(self):
        pass
    def mid_left_press_event(self):
        pass
    def mid_press_event(self):
        print("mid press")
        pass
    def mid_right_press_event(self):
        pass
    def down_left_press_event(self):
        pass
    def down_press_event(self):
        print("down press")
        pass
    def down_right_press_event(self):
        pass

    #release function
    def up_left_release_event(self):
        print("up_left release")
        pass
    def up_release_event(self):
        pass
    def up_right_release_event(self):
        pass
    def mid_left_release_event(self):
        pass
    def mid_release_event(self):
        print("mid release")
        pass
    def mid_right_release_event(self):
        pass
    def down_left_release_event(self):
        pass
    def down_release_event(self):
        print("down release")
        pass
    def down_right_release_event(self):
        pass




if __name__ == '__main__' :
    app = QApplication(sys.argv)

    login = LoginWindow()
    control = ControlWindow()

    #login.show()
    control.show()
    # a = QPushButton("Connect")
    # login.close()
    # app.exec_()

    sys.exit(app.exec_())
