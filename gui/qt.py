import sys
import time
import serial, subprocess
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
dotenv_path = Path('/home/pi/Documents/epani-test/.env')
load_dotenv(dotenv_path=dotenv_path)

try:
    serialport = serial.Serial(
        port=os.getenv('SERIAL_PORT'),
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
                subprocess.call(os.getenv('RUN_MAIN_COMMAND'), shell=True)

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
        self.ad_image_setup()
        self.ad_video_start()

        self.start = time.time()

        # TODO : QWidget::setLayout: Attempting to set QLayout "" on QStackedWidget "",which already has a layout

    def setup_screen(self):
        self.showFullScreen()
        self.setWindowFlags(Qt.FramelessWindowHint)
        QShortcut(QKeySequence('Ctrl+Q'), self).activated.connect(QApplication.instance().quit)

    def start_serial_worker_thread(self):
        self.worker = Worker()  # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        self.worker.moveToThread(
            self.thread)  # move the worker into the thread, do this first before connecting the signals

        self.thread.started.connect(self.worker.work)  # begin our worker object's loop when the thread starts running

        self.worker.intReady.connect(self.on_serial_worker_listen)
        # self.pushButton_2.clicked.connect(self.stop_loop)  # stop the loop on the stop button click

        self.worker.finished.connect(self.loop_finished)  # do something in the gui when the worker loop ends
        self.worker.finished.connect(self.thread.quit)  # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion

        self.thread.start()

    @staticmethod
    def loop_finished(self):
        print("worker closed do some processing if needed")
        return

    def stop_serial_worker_thread(self):
        self.worker.working = False

    def stack_ad_video_ui(self):
        self.instance = vlc.Instance('--input-repeat=999999')
        self.mediaplayer = self.instance.media_player_new()
        self.videoframe = QFrame(
            frameShape=QFrame.Box, frameShadow=QFrame.Raised
        )
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())

        ad_layout = QVBoxLayout()
        ad_layout.addWidget(self.videoframe)
        self.stackAdVideo.setLayout(ad_layout)

        file_name = os.getenv('AD_VIDEO_PATH')
        if file_name != '':
            media = self.instance.media_new(file_name)
            self.mediaplayer.set_media(media)

        self.vlc_events = self.mediaplayer.event_manager()
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.video_finished_callback, 1)

    def stack_main_ui(self):
        # Body Layout
        self.adImg = QLabel("ad_img")

        adImgSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        adImgSizePolicy.setHorizontalStretch(2)
        adImgSizePolicy.setVerticalStretch(0)
        adImgSizePolicy.setHeightForWidth(self.adImg.sizePolicy().hasHeightForWidth())

        self.adImg.setSizePolicy(adImgSizePolicy)
        # self.adImg.setMinimumSize(QSize(0, 500))
        # self.adImg.setStyleSheet(u"")
        # self.adImg.setPixmap(QPixmap(u":/newPrefix/Images/img.jfif"))
        self.adImg.setScaledContents(True)
        self.adImg.setAlignment(Qt.AlignCenter)

        # Main Content
        contentSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contentSizePolicy.setHorizontalStretch(1)
        contentSizePolicy.setVerticalStretch(0)

        contentW = QWidget()
        contentW.setStyleSheet(u"background: rgba( 58, 125, 242, 0.8 );\n"
                               "color:white;")
        contentW.setSizePolicy(contentSizePolicy)
        # contentW.setMinimumSize(QSize(630, 900))

        self.contentL = QVBoxLayout()
        self.contentL.setSpacing(0)
        self.contentL.setContentsMargins(0, 0, 0, 0)
        contentW.setLayout(self.contentL)

        bodyHorizontalLayout = QHBoxLayout()
        bodyHorizontalLayout.setSpacing(0)
        bodyHorizontalLayout.setContentsMargins(0, 0, 0, 0)

        bodyHorizontalLayout.addWidget(self.adImg)
        bodyHorizontalLayout.addWidget(contentW)

        # Footer Layout
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(0)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        create_footer_section(footer_layout)

        mainContentLayout = QVBoxLayout()
        mainContentLayout.setSpacing(0)
        mainContentLayout.setContentsMargins(0, 0, 0, 0)
        mainContentLayout.addLayout(bodyHorizontalLayout)
        mainContentLayout.addLayout(footer_layout)
        self.stackMain.setLayout(mainContentLayout)

    def init_layout(self):
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.setStyleSheet("border :None;")
        self.setCentralWidget(self.stackedWidget)

        self.stackAdVideo = QWidget()
        self.stackAdVideo.showFullScreen()

        self.stackMain = QWidget()
        self.stackMain.showFullScreen()

        self.stack_ad_video_ui()
        self.stack_main_ui()

        self.stackedWidget.addWidget(self.stackAdVideo)
        self.stackedWidget.addWidget(self.stackMain)
        self.stackedWidget.showFullScreen()

        main_layout = QVBoxLayout()
        self.stackedWidget.setLayout(main_layout)
        #main_layout.addWidget(self.stackedWidget)
        #self.setLayout(main

    def ad_image_setup(self):
        ad_img_path = os.getenv('AD_IMAGE_PATH')
        if ad_img_path:
            ad_img = QPixmap(ad_img_path)
            self.adImg.setPixmap(ad_img)

    @callbackmethod
    def video_finished_callback(self, *args, **kwargs):
        # self.mediaplayer.stop()
        self.ad_video_start()

    def ad_video_start(self):
        self.mediaplayer.set_fullscreen(True)
        # self.mediaplayer.audio_set_mute(True)
        self.mediaplayer.play()
        serial_write("advideo")

    def ad_video_stop(self):
        self.mediaplayer.stop()

    def toggle_ad_video(self):

        if self.stackAdVideo == self.stackedWidget.currentWidget():
            self.ad_video_stop()
            serialport.flushInput()
            serialport.flushOutput()
            serialport.flush()
            # time.sleep(1)
            self.stackedWidget.setCurrentWidget(self.stackMain)
        else:
            self.stackedWidget.setCurrentWidget(self.stackAdVideo)
            # time.sleep(1)
            self.ad_video_start()

    def volume_selection(self, data):
        if not self.currOrder.is_volume_set():
            if data not in ['O', 'T', 'F']:
                return

            if data == 'O':
                self.currOrder.set_volume('1', 5)
            elif data == 'T':
                self.currOrder.set_volume('2', 10)
            elif data == 'F':
                self.currOrder.set_volume('5', 15)

            serial_write("readcard")
            toggle_content_screen(self.contentL, "insertCard", order=self.currOrder)

            return

    def read_card(self, data):
        if not self.currOrder.is_card_set():
            if 9 > len(data) > 5:
                self.currOrder.set_cardno(data)

                serial_write("cardok")
                payment_status = self.currOrder.process_payment()
                # TODO : PROCESSING PAYMENT SCREEN IS NOT BEING SHOWN
                # toggle_content_screen(self.contentL, "processingPayment")

                if payment_status == "payment_done":
                    time.sleep(2)  # Necessary delay for serial here
                    serial_write("tapp")
                    toggle_content_screen(self.contentL, "tapSelection")
                for i in range(5):
                    print(payment_status)
            return


    def tap_selection(self, data):
        if not self.currOrder.is_tap_set():
            if data not in ['1', '2', '3', '4']:
                return

            if data == '1':
                self.currOrder.set_tap('1')

            elif data == '2':
                self.currOrder.set_tap('2')

            elif data == '3':
                self.currOrder.set_tap('3')

            elif data == '4':
                self.currOrder.set_tap('4')

            serial_write("dispense")
            toggle_content_screen(self.contentL, "dispensingWater", order=self.currOrder)
            self.currOrder.print_all()
            # TODO : NAVIGATING TO AD SCREEN WHEN 'C' IS PRESSED WHILE DISPENSING

    def on_serial_worker_listen(self, data):
        

        if data == "":
            # TODO : See if this can be removed
            if self.stackAdVideo == self.stackedWidget.currentWidget():
                self.start = time.time()
                return

            stop = time.time()
            if stop - self.start > 90.0:
                self.currOrder = None
                self.start = time.time()
                self.toggle_ad_video()
            return

        self.start = time.time()

        if self.stackAdVideo == self.stackedWidget.currentWidget():
            self.toggle_ad_video()

            serial_write("volume")
            toggle_content_screen(self.contentL, "volumeSelection")
            return

        if self.currOrder is None:
            self.currOrder = Order()

        # for volume selection
        self.volume_selection(data)

        if data == 'C':
            self.currOrder = None
            self.toggle_ad_video()
            return

        try:
            # for reading card
            self.read_card(data)
        except Exception as e:
            f = open("demofile2.txt", "w")
            f.write(e)
            f.close()

        # for tap selection
        self.tap_selection(data)

        if 'z' in data:
            self.currOrder.dispensed_volume = data[1:]
            print(self.currOrder.dispensed_volume)

        if data == "dispensed":
            time.sleep(2)
            self.currOrder = None
            self.toggle_ad_video()
            return




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        app.exec_()
    except Exception as e:
        print(e)
        print("Exiting ")
        
