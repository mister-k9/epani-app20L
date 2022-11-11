import sys
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QLabel, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, QtCore, QtNetwork
import requests
import time

file = "epani.db"

class CheckConnectivity(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        url = QtCore.QUrl("https://www.google.com/")
        req = QtNetwork.QNetworkRequest(url)
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.res = self.net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)
        self.msg = QtWidgets.QMessageBox()

    @QtCore.pyqtSlot()
    def processRes(self):
        if self.res.bytesAvailable():
            self.msg.information(None, "Info", "You are connected to the Internet.")
        self.res.deleteLater()

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply.NetworkError)
    def processErr(self, code):
        self.msg.critical(None, "Info", "You are not connected to the Internet.")
        print(code)

class MainWindow(QMainWindow, QtCore.QObject):
    def __init__(self):
        super().__init__()
        #self.showFullScreen()

        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)

        self.label = QLabel()
        self.label.setText("Started Executing E-Pani App")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('background:black;color:white;')
        self.label.setFont(font)
        self.setCentralWidget(self.label)
        self.internet_available = False
        self.show()
        
        self.delay(2)
        self.start_app()
        
    def delay(self, seconds):
        millisecs = seconds*1000
        loop = QEventLoop()
        QTimer.singleShot(millisecs, loop.quit)
        loop.exec_()

    def start_app(self):
        print("K9")
        while not self.internet_available:
            self.check_internet_connection()

    @QtCore.pyqtSlot()
    def processRes(self):
        if self.res.bytesAvailable():
            print("Info", "You are connected to the Internet.")
            self.label.setText("You are connected to the Internet.")
            self.internet_available = True
        self.res.deleteLater()

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply.NetworkError)
    def processErr(self, code):
        print("Info", "You are not connected to the Internet.")
        self.label.setText("You are not connected to the Internet.")
        self.internet_available = False

    def check_internet_connection(self, duration=None):
        url = QtCore.QUrl("https://www.google.com/")
        req = QtNetwork.QNetworkRequest(url)
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.res = self.net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)

    def check_server_connection(self, duration=None):
        url = QtCore.QUrl("https://epani-django.herokuapp.com/")
        req = QtNetwork.QNetworkRequest(url)
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.res = self.net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)


    


        
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.showFullScreen()
    window.show()
    try:
        app.exec_()
    except Exception as e:
        print(e)
        print("Exiting ")
        
