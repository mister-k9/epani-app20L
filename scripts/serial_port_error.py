from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)

        self.label = QLabel("The Machine Is Not Working,\nPlease Contact Service Center.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('background:black;color:white;')
        self.label.setFont(font)
        self.setCentralWidget(self.label)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    app.exec_()
