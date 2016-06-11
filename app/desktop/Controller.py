#-*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
author : Walon Li
"""

import sys
import urllib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtWidgets import QOpenGLWidget, QAction, QShortcut, QGridLayout, QDialog
import socket
from ClientSocket import ClientSocket
from PyQt5.uic import loadUi
from PyQt5.QtGui  import *
from PyQt5.QtCore import *
import numpy as np
import cv2

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


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__(None)

        # connet button
        self._btn = QPushButton("Connect")
        self._btn.setFixedSize(140, 30)
        self._btn.clicked.connect(self._connectPi)

        # ip text editor
        self._ipText = QTextEdit("192.168.1.110")
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




class WebCamView(QWidget):
    def __init__(self, parent=None):
        super(WebCamView, self).__init__(parent)

        #self.cvImage = cv2.imread(r'cat.jpg')
        #self.resize(600, 400)
        self.cap = cv2.VideoCapture("http://192.168.1.110:8080/?action=stream?dummy=param.mjpg")
        self.startTimer(100)

        #ret, self.cvImage = self.cap.read()

        #self.height, self.width, self.byteValue = self.cvImage.shape
        #self.byteValue = self.byteValue * self.width

        #cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)
        #cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2GRAY)
        #self.mQImage = QImage(self.cvImage, self.width, self.height, self.byteValue, QImage.Format_RGB888)

    def timerEvent(self, QTimerEvent):
        self.repaint()

    def paintEvent(self, QPaintEvent):
        ret, cvImage = self.cap.read()
        height, width, byteValue = cvImage.shape
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)

        byteValue = byteValue * width
        mQImage = QImage(cvImage, width, height, byteValue, QImage.Format_RGB888)

        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, mQImage)
        painter.end()

    #def keyPressEvent(self, QKeyEvent):
    #    app.exit(1)
        #super(MyDialog, self).keyPressEvent(QKeyEvent)
        #if 's' == QKeyEvent.text():
        #else:



class ControlWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(None)

        self._host = ""
        self._port = 0
        self._cam  = WebCamView(self)

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
        press_event = [self.upLeftPressEvent, self.upPressEvent, self.upRightPressEvent,
                       self.midLefPressEvent, self.midPressEvent, self.midRightPressEvent,
                       self.downLeftPressEvent, self.downPressEvent, self.downRightPressEvent]
        release_event = [self.upLeftReleaseEvent, self.upReleaseEvent, self.upRightReleaseEvent,
                         self.midLeftReleaseEvent, self.midReleaseEvent, self.midRightReleaseEvent,
                         self.downLeftReleaseEvent, self.downReleaseEvent, self.downRightReleaseEvent]

        # set position and connect event
        p = QPoint(620, 420) # start point
        for i in range(len(btn_grp)):
            btn_grp[i].setFixedSize(QSize(50, 50))
            btn_grp[i].move(p)
            btn_grp[i].pressed.connect(press_event[i])
            btn_grp[i].released.connect(release_event[i])
            btn_grp[i].setFocusPolicy(Qt.NoFocus)
            if p.x() >= 740:
                p.setX(620)
                p.setY(p.y()+60)
            else:
                p.setX(p.x()+60)

        #act = QAction("Action", self._up_left, )
        #self._up_left.setShortcut(Qt.Key_Up)

        #self._up_left.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        #self._up_left.shortcut.activated.connect(self.)

        #self._up_left.setAutoRepeat(False)
        #self._up_left.addAction()
        #self._up.clicked.connect(self.send_event)

        #self._graphic = QOpenGLWidget(self)
        #self._graphic.setFixedSize(QSize(500, 400))
        #self._graphic.move(QPoint(10, 10))
        self._cam.setFixedSize(QSize(500, 400))
        self._cam.move(QPoint(10, 10))

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
        self._host = host
        self._port = port
        return self._sock.connect(host, port)

    def sendEvent(self, data):
        while self._sock.sendAction(data) == False:
            try:
                print("reconnect...", self._host, self._port)
                self._sock.close()
                self._sock = ClientSocket()
                self.bindSocket(self._host, self._port)
            except:
                time.sleep(4)
    """
    def event(self, e):
        if type(e) == QKeyEvent and not e.isAutoRepeat():
            if e.key() == Qt.Key_Up:
                print("123")
                return True

        #print(type(e))
        return QWidget.event(self, e)
    """

    def keyPressEvent(self, e):
        if not e.isAutoRepeat():
            obj = None
            if e.key() == Qt.Key_Up:
                obj = self._up
            elif e.key() == Qt.Key_Left:
                obj = self._mid_left
            elif e.key() == Qt.Key_Right:
                obj = self._mid_right
            elif e.key() == Qt.Key_Down:
                obj = self._down
            if obj != None:
                obj.setDown(True)
                obj.pressed.emit()
            else:
                QWidget.keyPressEvent(self, e)
        else:
            QWidget.keyPressEvent(self, e)

    def keyReleaseEvent(self, e):
        if not e.isAutoRepeat():
            obj = None
            if e.key() == Qt.Key_Up:
                obj = self._up
            elif e.key() == Qt.Key_Left:
                obj = self._mid_left
            elif e.key() == Qt.Key_Right:
                obj = self._mid_right
            elif e.key() == Qt.Key_Down:
                obj = self._down
            if obj != None:
                obj.setDown(False)
                obj.released.emit()
            else:
                QWidget.keyPressEvent(self, e)
        else:
            QWidget.keyReleaseEvent(self, e)

    #press function
    def upLeftPressEvent(self):
        pass
    def upPressEvent(self):
        print("up press")
        self.sendEvent("arrow-key:up action:press")
        pass
    def upRightPressEvent(self):
        pass
    def midLefPressEvent(self):
        print("mid-left press")
        self.sendEvent("arrow-key:mid-left action:press")
        pass
    def midPressEvent(self):
        pass
    def midRightPressEvent(self):
        print("mid-right press")
        self.sendEvent("arrow-key:mid-right action:press")
        pass
    def downLeftPressEvent(self):
        pass
    def downPressEvent(self):
        print("down press")
        self.sendEvent("arrow-key:down action:press")
        pass
    def downRightPressEvent(self):
        pass

    #release function
    def upLeftReleaseEvent(self):
        pass
    def upReleaseEvent(self):
        print("up release")
        self.sendEvent("arrow-key:up action:release")
        pass
    def upRightReleaseEvent(self):
        pass
    def midLeftReleaseEvent(self):
        print("mid-left release")
        self.sendEvent("arrow-key:mid-left action:release")
        pass
    def midReleaseEvent(self):
        pass
    def midRightReleaseEvent(self):
        print("mid-right release")
        self.sendEvent("arrow-key:mid-right action:release")
        pass
    def downLeftReleaseEvent(self):
        pass
    def downReleaseEvent(self):
        print("down release")
        self.sendEvent("arrow-key:down action:release")
        pass
    def downRightReleaseEvent(self):
        print("send fake close")
        self.sendEvent("close")
        pass







if __name__ == '__main__' :
    app = QApplication(sys.argv)

    login = LoginWindow()
    control = ControlWindow()

    login.show()

    #control.show()

    # login.close()
    #app.exec_()
    #cap = cv2.VideoCapture(0)
    # powerful open cv...
    #cap = cv2.VideoCapture("http://192.168.1.10:8080/?action=stream?dummy=param.mjpg")

    #w = MyDialog()
    #w.resize(600, 400)
    #w.show()
    app.exec_()

