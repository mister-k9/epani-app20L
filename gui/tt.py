import sys
import time
import serial
import subprocess
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QStackedWidget, QSizePolicy, QShortcut, QApplication, QFrame

from classes.order import Order
from classes.ui import create_footer_section, toggle_content_screen

import vlc
from vlc import callbackmethod
import os
from dotenv import load_dotenv
from pathlib import Path
# dotenv_path = Path('/home/epani/Desktop/epani-app20L/.env')
# load_dotenv(dotenv_path=dotenv_path)

try:
    serialport = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=0.3
    )
except Exception as e:
    print(e)


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def work(self):
        print("Worker Started")
        serialport.flushInput()
        serialport.flushOutput()
        while self.working:
            try:
                line = serialport.readline().decode('utf-8').rstrip()
                self.intReady.emit(line)
            except Exception as e:
                print(e)
                self.working = False
                serialport.close()
                window.close()
                # subprocess.call(os.getenv('RUN_MAIN_COMMAND'), shell=True)

        self.finished.emit()
        print('Worker Finished')


def serial_write(text):
    serialport.write(text.encode('utf-8'))
    print(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedWidget = None
        self.stackMain = None
        self.stackAdVideo = None
        self.currOrder = None
        self.adVideoWidget = None
        self.thread = None
        self.worker = None

        self.setup_screen()
        self.start_serial_worker_thread()
        self.init_layout()
        # self.ad_image_setup()
        self.ad_video_start()

        self.start = time.time()

        # TODO : QWidget::setLayout: Attempting to set QLayout "" on QStackedWidget "",which already has a layout

    def setup_screen(self):
        self.showFullScreen()
        self.setWindowFlags(Qt.FramelessWindowHint)
        QShortcut(QKeySequence('Ctrl+Q'),
                  self).activated.connect(QApplication.instance().quit)

    def start_serial_worker_thread(self):
        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(
            self.thread)  # move the worker into the thread, do this first before connecting the signals

        # begin our worker object's loop when the thread starts running
        self.thread.started.connect(self.worker.work)

        self.worker.intReady.connect(self.on_serial_worker_listen)
        # self.pushButton_2.clicked.connect(self.stop_loop)  # stop the loop on the stop button click

        # do something in the gui when the worker loop ends
        self.worker.finished.connect(self.loop_finished)
        # tell the thread it's time to stop running
        self.worker.finished.connect(self.thread.quit)
        # have worker mark itself for deletion
        self.worker.finished.connect(self.worker.deleteLater)
        # have thread mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @staticmethod
    def loop_finished(self):
        print("worker closed do some processing if needed")
        return

    def stop_serial_worker_thread(self):
        self.worker.working = False

    def init_layout(self):
        self.mainWidget = QWidget()
        # self.mainWidget.showFullScreen()
        self.adVideoWidget = QWidget()
        # self.adVideoWidget.showFullScreen()

        # self.adImg = QLabel("ad_img")
        # adImgSizePolicy = QSizePolicy(
        #     QSizePolicy.Expanding, QSizePolicy.Expanding)
        # adImgSizePolicy.setHorizontalStretch(2)
        # adImgSizePolicy.setVerticalStretch(0)
        # adImgSizePolicy.setHeightForWidth(
        #     self.adImg.sizePolicy().hasHeightForWidth())
        # self.adImg.setSizePolicy(adImgSizePolicy)
        # # self.adImg.setMinimumSize(QSize(0, 500))
        # # self.adImg.setStyleSheet(u"")
        # # self.adImg.setPixmap(QPixmap(u":/newPrefix/Images/img.jfif"))
        # self.adImg.setScaledContents(True)
        # self.adImg.setAlignment(Qt.AlignCenter)

        # Ad Video
        self.instance = vlc.Instance('--input-repeat=999999')
        self.mediaplayer = self.instance.media_player_new()
        self.videoframe = QFrame(
            frameShape=QFrame.Box, frameShadow=QFrame.Raised
        )
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        ad_layout = QVBoxLayout()
        ad_layout.addWidget(self.videoframe)
        self.adVideoWidget.setLayout(ad_layout)

        file_name = 'media/zomato-ad.avi'
        if file_name != '':
            media = self.instance.media_new(file_name)
            self.mediaplayer.set_media(media)

        self.vlc_events = self.mediaplayer.event_manager()
        self.vlc_events.event_attach(
            vlc.EventType.MediaPlayerEndReached, self.video_finished_callback, 1)



        # Main Content
        contentSizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        contentSizePolicy.setHorizontalStretch(1)
        contentSizePolicy.setVerticalStretch(0)
        contentWidget = QWidget()
        contentWidget.setStyleSheet("background: rgba( 58, 125, 242, 0.8 );color:white;")
        contentWidget.setSizePolicy(contentSizePolicy)
        # contentW.setMinimumSize(QSize(630, 900))
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        contentWidget.setLayout(self.contentLayout)

        bodyHorizontalLayout = QHBoxLayout()
        bodyHorizontalLayout.setSpacing(0)
        bodyHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        bodyHorizontalLayout.addWidget(self.adVideoWidget)
        bodyHorizontalLayout.addWidget(contentWidget)

        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(0)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        create_footer_section(footer_layout)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addLayout(footer_layout)
        mainLayout.addLayout(bodyHorizontalLayout)
        self.mainWidget.setLayout(mainLayout)
        self.setCentralWidget(self.mainWidget)

    @callbackmethod
    def video_finished_callback(self, *args, **kwargs):
        # self.mediaplayer.stop()
        self.ad_video_start()

    def ad_video_start(self):
        # self.mediaplayer.set_fullscreen(True)
        # self.mediaplayer.audio_set_mute(True)
        self.mediaplayer.play()
        serial_write("advideo")

    def ad_video_stop(self):
        self.mediaplayer.stop()





    def on_serial_worker_listen(self, data):
        #print(data)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        app.exec_()
    except Exception as e:
        print(e)
        print("Exiting ")
