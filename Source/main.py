from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from convertor import Ui_MainWindow
import datetime
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import _thread
from PIL import Image


class Convertor(QMainWindow):
    language_handle = "close"
    info_handle = "close"
    theme_handle = "close"
    fileAddress_mp4_mp3 = ""
    savefile_mp4_mp3 = ""
    video = None
    fileAddress_jpg_png = ""
    savefile_jpg_png = ""
    photo_jpg_png = None
    fileAddress_png_jpg = ""
    savefile_png_jpg = ""
    photo_png_jpg = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Convertor")
        self.setWindowIcon(QIcon(r"2x\mainPhoto.jfif"))

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.frame_info.hide()
        self.ui.theme_frame.hide()
        self.ui.language_frame.hide()
        self.ui.mp4_mp3_lineEdit_time.setReadOnly(True)
        self.ui.mp4_mp3_lineEdit_size.setReadOnly(True)
        self.ui.mp4_mp3_lineEdit_newSize.setReadOnly(True)
        self.ui.btn_mp4_mp3_convert.setEnabled(False)
        self.ui.btn_convert_jpg_png.setEnabled(False)
        self.ui.btn_convert_png_jpg.setEnabled(False)
        self.ui.process_label.setText("")
        self.ui.process_label_jpg_png.setText("")
        self.ui.process_label_png_jpg.setText("")

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.btn_mp4_mp3.clicked.connect(self.mp4_mp3)
        self.ui.btn_home.clicked.connect(self.home_func)
        self.ui.btn_setting.clicked.connect(self.setting)
        self.ui.btn_png_jpg.clicked.connect(self.png_jpg)
        self.ui.btn_jpg_png.clicked.connect(self.jpg_png)

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def home_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def mp4_mp3(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.mp4tomp3)
        self.ui.btn_browse_mp4_mp3_address.clicked.connect(self.browse_fileAddress_mp4_mp3)
        self.ui.btn_browse_mp4_mp3_save.clicked.connect(self.browse_save_mp4_mp3)
        self.ui.btn_mp4_mp3_convert.clicked.connect(self.convert_mp4_mp3_func)
        self.ui.btn_mp4_mp3_clear.clicked.connect(self.clear_mp4_mp3_func)

    def jpg_png(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.jpgtopng)
        self.ui.btn_browse_jpg_png_address.clicked.connect(self.browse_fileAddress_jpg_png)
        self.ui.btn_browse_jpg_png_save.clicked.connect(self.browse_save_jpg_png)
        self.ui.btn_convert_jpg_png.clicked.connect(self.convert_jpg_png)
        self.ui.btn_clear_jpg_png.clicked.connect(self.clear_jpg_png)

    def png_jpg(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.pngtojpg)
        self.ui.btn_browse_png_jpg_address.clicked.connect(self.browse_fileAddress_png_jpg)
        self.ui.btn_browse_png_jpg_save.clicked.connect(self.browse_save_png_jpg)
        self.ui.btn_convert_png_jpg.clicked.connect(self.convert_png_jpg)
        self.ui.btn_clear_png_jpg.clicked.connect(self.clear_png_jpg)

    def setting(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)
        self.ui.btn_info.clicked.connect(self.info_func)
        self.ui.btn_language.clicked.connect(self.language_func)
        self.ui.btn_theme.clicked.connect(self.theme_func)
        self.ui.btn_english.clicked.connect(self.english_language)
        self.ui.btn_persian.clicked.connect(self.persian_language)
        self.ui.btn_germany.clicked.connect(self.german_language)
        self.ui.btn_russian.clicked.connect(self.russian_language)

    def info_func(self):
        if self.info_handle == "close":
            self.ui.frame_info.show()
            self.animation_func(self.ui.frame_info, 20, 80, 341, 171, True)
            self.info_handle = "open"
        elif self.info_handle == "open":
            self.animation_func(self.ui.frame_info, 20, 80, 341, 171, False)
            self.info_handle = "close"

    def language_func(self):
        if self.language_handle == "close":
            self.ui.language_frame.show()
            self.animation_func(self.ui.language_frame, 370, 260, 291, 131, True)
            self.language_handle = "open"
        elif self.language_handle == "open":
            self.animation_func(self.ui.language_frame, 370, 260, 291, 131, False)
            self.language_handle = "close"

    def theme_func(self):
        if self.theme_handle == "close":
            self.ui.theme_frame.show()
            self.animation_func(self.ui.theme_frame, 20, 260, 341, 131, True)
            self.theme_handle = "open"
        elif self.theme_handle == "open":
            self.animation_func(self.ui.theme_frame, 20, 260, 341, 131, False)
            self.theme_handle = "close"

    def animation_func(self, frame, x, y, width, height, openState):
        if openState:
            self.anim = QPropertyAnimation(frame, b"geometry")
            self.anim.setDuration(500)
            self.anim.setStartValue(QRect(x, y, 0, height))
            self.anim.setEndValue(QRect(x, y, width, height))
            self.anim.start()
        else:
            self.anim = QPropertyAnimation(frame, b"geometry")
            self.anim.setDuration(500)
            self.anim.setStartValue(QRect(x, y, width, height))
            self.anim.setEndValue(QRect(x, y, 0, height))
            self.anim.start()

    def showError(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Critical)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def showInfo(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def browse_fileAddress_mp4_mp3(self):
        self.fileAddress_mp4_mp3 = QFileDialog.getOpenFileNames(
            self, "Select the mp4 file", "C:/Users/sajjad/Desktop", "source File (*.mov *.mp4)")
        self.ui.mp4_mp3_lineEdit_address.setText(self.fileAddress_mp4_mp3[0][0])
        self.setDetails_mp4_mp3()
        self.ui.btn_mp4_mp3_convert.setEnabled(True)

    def browse_save_mp4_mp3(self):
        self.savefile_mp4_mp3 = QFileDialog.getExistingDirectory(
            self, "Select directory", "C:/Users/sajjad/Desktop")
        self.ui.mp4_mp3_lineEdit_save.setText(self.savefile_mp4_mp3)

    def setDetails_mp4_mp3(self):
        self.video = VideoFileClip(self.fileAddress_mp4_mp3[0][0])
        name = os.path.basename(self.fileAddress_mp4_mp3[0][0])
        name = os.path.splitext(name)[0]
        self.ui.mp4_mp3_lineEdit_name.setText(name)
        size = os.path.getsize(self.fileAddress_mp4_mp3[0][0]) / 1000000
        size = round(size, 1)
        self.ui.mp4_mp3_lineEdit_size.setText(str(size) + " MB")
        time = str(datetime.timedelta(seconds=int(self.video.duration)))
        self.ui.mp4_mp3_lineEdit_time.setText(time)

    def convert_mp4_mp3_func(self):
        if len(self.savefile_mp4_mp3) != 0:
            if len(self.ui.mp4_mp3_lineEdit_name.text()) != 0:
                self.ui.process_label.setText("Process is started...")
                _thread.start_new_thread(self.process_mp4_mp3, (2,))
            else:
                self.showError("Name", "You should fill name's lineEdit.")
        else:
            self.showError("Save file", "You should choose directory to save file.")

    def process_mp4_mp3(self, num):
        try:
            audioFile = self.video.audio
            filename = self.savefile_mp4_mp3 + "/" + self.ui.mp4_mp3_lineEdit_name.text() + ".mp3"
            audioFile.write_audiofile(filename)
            size = os.path.getsize(filename) / 1000000
            size = round(size, 1)
            self.ui.mp4_mp3_lineEdit_newSize.setText(str(size) + " MB")
            self.ui.process_label.setText("Process is finish.")
        except:
            self.ui.process_label.setText("Something went wrong...")

    def clear_mp4_mp3_func(self):
        self.ui.mp4_mp3_lineEdit_save.setText("")
        self.ui.mp4_mp3_lineEdit_address.setText("")
        self.ui.mp4_mp3_lineEdit_name.setText("")
        self.ui.mp4_mp3_lineEdit_size.setText("")
        self.ui.mp4_mp3_lineEdit_newSize.setText("")
        self.ui.mp4_mp3_lineEdit_time.setText("")
        self.ui.btn_mp4_mp3_convert.setEnabled(False)
        self.ui.process_label.setText("")

    def browse_fileAddress_jpg_png(self):
        self.fileAddress_jpg_png = QFileDialog.getOpenFileNames(
            self, "Select a photo", "C:/Users/sajjad/Desktop", "source File (*.jpg)")
        self.ui.jpg_png_lineEdit_address.setText(self.fileAddress_jpg_png[0][0])
        self.setDetails_jpg_png()
        self.ui.btn_convert_jpg_png.setEnabled(True)

    def browse_save_jpg_png(self):
        self.savefile_jpg_png = QFileDialog.getExistingDirectory(
            self, "Select directory", "C:/Users/sajjad/Desktop")
        self.ui.jpg_png_lineEdit_save.setText(self.savefile_jpg_png)

    def setDetails_jpg_png(self):
        self.photo_jpg_png = Image.open(self.fileAddress_jpg_png[0][0])
        name = os.path.basename(self.fileAddress_jpg_png[0][0])
        name = os.path.splitext(name)[0]
        self.ui.jpg_png_lineEdit_name.setText(name)
        self.ui.photo_jpg_png.setPixmap(QPixmap(self.fileAddress_jpg_png[0][0]))

    def clear_jpg_png(self):
        self.ui.jpg_png_lineEdit_save.setText("")
        self.ui.jpg_png_lineEdit_address.setText("")
        self.ui.jpg_png_lineEdit_name.setText("")
        self.ui.photo_jpg_png.setPixmap(QPixmap())
        self.ui.btn_convert_jpg_png.setEnabled(False)

    def convert_jpg_png(self):
        if len(self.savefile_jpg_png) != 0:
            if len(self.ui.jpg_png_lineEdit_name.text()) != 0:
                self.ui.process_label_jpg_png.setText("Process is started...")
                _thread.start_new_thread(self.process_jpg_png, (2,))
        else:
            self.showError("Save address", "You should choose an address to save file.")

    def process_jpg_png(self, num):
        try:
            filename = self.savefile_jpg_png + "/" + self.ui.jpg_png_lineEdit_name.text() + ".png"
            self.photo_jpg_png.save(filename)
            self.ui.process_label_jpg_png.setText("Process is finish.")
        except:
            self.ui.process_label_jpg_png.setText("Something went wrong...")

    def browse_fileAddress_png_jpg(self):
        self.fileAddress_png_jpg = QFileDialog.getOpenFileNames(
            self, "Select a photo", "C:/Users/sajjad/Desktop", "source File (*.png)")
        self.ui.png_jpg_lineEdit_address.setText(self.fileAddress_png_jpg[0][0])
        self.setDetails_png_jpg()
        self.ui.btn_convert_png_jpg.setEnabled(True)

    def browse_save_png_jpg(self):
        self.savefile_png_jpg = QFileDialog.getExistingDirectory(
            self, "Select directory", "C:/Users/sajjad/Desktop")
        self.ui.png_jpg_lineEdit_save.setText(self.savefile_png_jpg)

    def setDetails_png_jpg(self):
        self.photo_png_jpg = Image.open(self.fileAddress_png_jpg[0][0])
        name = os.path.basename(self.fileAddress_png_jpg[0][0])
        name = os.path.splitext(name)[0]
        self.ui.png_jpg_lineEdit_name.setText(name)
        self.ui.photo_png_jpg.setPixmap(QPixmap(self.fileAddress_png_jpg[0][0]))

    def clear_png_jpg(self):
        self.ui.png_jpg_lineEdit_save.setText("")
        self.ui.png_jpg_lineEdit_address.setText("")
        self.ui.png_jpg_lineEdit_name.setText("")
        self.ui.photo_png_jpg.setPixmap(QPixmap())
        self.ui.btn_convert_png_jpg.setEnabled(False)

    def convert_png_jpg(self):
        if len(self.savefile_png_jpg) != 0:
            if len(self.ui.png_jpg_lineEdit_name.text()) != 0:
                self.ui.process_label_png_jpg.setText("Process is started...")
                _thread.start_new_thread(self.process_png_jpg, (2,))
        else:
            self.showError("Save address", "You should choose an address to save file.")

    def process_png_jpg(self, num):
        try:
            filename = self.savefile_png_jpg + "/" + self.ui.png_jpg_lineEdit_name.text() + ".jpg"
            self.photo_png_jpg.save(filename)
            self.ui.process_label_png_jpg.setText("Process is finish.")
        except:
            self.ui.process_label_png_jpg.setText("Something went wrong...")

    def english_language(self):
        _translate = QCoreApplication.translate
        self.ui.home_label.setText(_translate("MainWindow", "Welcome"))
        self.ui.btn_mp4_mp3.setText(_translate("MainWindow", "Mp4 to Mp3"))
        self.ui.btn_jpg_png.setText(_translate("MainWindow", "Jpg to Png"))
        self.ui.btn_png_jpg.setText(_translate("MainWindow", "Png to Jpg"))
        self.ui.btn_setting.setText(_translate("MainWindow", "Setting"))
        self.ui.fileaddress_label_mp4_mp3.setText(_translate("MainWindow", "File address :"))
        self.ui.label_mp4_mp3.setText(_translate("MainWindow", "Convert Mp4 to Mp3"))
        self.ui.btn_browse_mp4_mp3_address.setText(_translate("MainWindow", "Choose"))
        self.ui.savefile_label_mp4_mp3.setText(_translate("MainWindow", "Save as  :"))
        self.ui.btn_browse_mp4_mp3_save.setText(_translate("MainWindow", "Choose"))
        self.ui.name_label_mp4_mp3.setText(_translate("MainWindow", "Name  :"))
        self.ui.time_label_mp4_mp3_2.setText(_translate("MainWindow", "Time  :"))
        self.ui.size_label_mp4_mp3.setText(_translate("MainWindow", "Size  :"))
        self.ui.btn_mp4_mp3_convert.setText(_translate("MainWindow", "Convert"))
        self.ui.btn_mp4_mp3_clear.setText(_translate("MainWindow", "Clear"))
        self.ui.newsize_label_mp4_mp3.setText(_translate("MainWindow", "New size  :"))
        self.ui.btn_browse_jpg_png_address.setText(_translate("MainWindow", "Choose"))
        self.ui.btn_browse_jpg_png_save.setText(_translate("MainWindow", "Choose"))
        self.ui.save_label_jpg_png.setText(_translate("MainWindow", "Save as  :"))
        self.ui.fileaddress_label_jpg_png_2.setText(_translate("MainWindow", "File address :"))
        self.ui.name_label_jpg_png.setText(_translate("MainWindow", "Name  :"))
        self.ui.label_jpg_png.setText(_translate("MainWindow", "Convert Jpg to Png"))
        self.ui.btn_clear_jpg_png.setText(_translate("MainWindow", "Clear"))
        self.ui.btn_convert_jpg_png.setText(_translate("MainWindow", "Convert"))
        self.ui.save_label_png_jpg.setText(_translate("MainWindow", "Save as  :"))
        self.ui.fileaddress_label_png_jpg.setText(_translate("MainWindow", "File address :"))
        self.ui.btn_browse_png_jpg_address.setText(_translate("MainWindow", "Choose"))
        self.ui.name_label_png_jpg.setText(_translate("MainWindow", "Name  :"))
        self.ui.btn_clear_png_jpg.setText(_translate("MainWindow", "Clear"))
        self.ui.btn_convert_png_jpg.setText(_translate("MainWindow", "Convert"))
        self.ui.btn_browse_png_jpg_save.setText(_translate("MainWindow", "Choose"))
        self.ui.label_png_jpg.setText(_translate("MainWindow", "Convert Png to Jpg"))
        self.ui.label_setting.setText(_translate("MainWindow", "Setting"))
        self.ui.label_info.setText(_translate("MainWindow", "Powered by : Sajjad fani\n"
                                                            "Language : Python 3.9\n"
                                                            "Telegram ID : @sajad_fani\n"
                                                            "Email : faniam321@gmail.com"))
        self.ui.btn_info.setText(_translate("MainWindow", "Info"))
        self.ui.btn_theme.setText(_translate("MainWindow", "Theme"))
        self.ui.theme_1.setToolTip(_translate("MainWindow", "Theme 1"))
        self.ui.theme_3.setToolTip(_translate("MainWindow", "Theme 3"))
        self.ui.theme_2.setToolTip(_translate("MainWindow", "Theme 2"))
        self.ui.theme_4.setToolTip(_translate("MainWindow", "Theme 4"))
        self.ui.theme_6.setToolTip(_translate("MainWindow", "Theme 6"))
        self.ui.theme_5.setToolTip(_translate("MainWindow", "Theme 5"))
        self.ui.btn_language.setText(_translate("MainWindow", "Language"))
        self.ui.btn_home.setToolTip(_translate("MainWindow", "Home"))

    def persian_language(self):
        _translate = QCoreApplication.translate
        self.ui.home_label.setText(_translate("MainWindow", "خوش آمدید"))
        self.ui.btn_mp4_mp3.setText(_translate("MainWindow", "فیلم به اهنگ"))
        self.ui.btn_setting.setText(_translate("MainWindow", "تنظیمات"))
        self.ui.fileaddress_label_mp4_mp3.setText(_translate("MainWindow", ": آدرس فایل "))
        self.ui.label_mp4_mp3.setText(_translate("MainWindow", "تبدیل فیلم به اهنگ"))
        self.ui.btn_browse_mp4_mp3_address.setText(_translate("MainWindow", "جستجو"))
        self.ui.savefile_label_mp4_mp3.setText(_translate("MainWindow", ": ذخیره در "))
        self.ui.btn_browse_mp4_mp3_save.setText(_translate("MainWindow", "جستجو"))
        self.ui.name_label_mp4_mp3.setText(_translate("MainWindow", ": اسم"))
        self.ui.time_label_mp4_mp3_2.setText(_translate("MainWindow", ": زمان"))
        self.ui.size_label_mp4_mp3.setText(_translate("MainWindow", ": اندازه"))
        self.ui.btn_mp4_mp3_convert.setText(_translate("MainWindow", "تبدیل کردن"))
        self.ui.btn_mp4_mp3_clear.setText(_translate("MainWindow", "پاک کردن"))
        self.ui.newsize_label_mp4_mp3.setText(_translate("MainWindow", ": اندازه جدید"))
        self.ui.btn_browse_jpg_png_address.setText(_translate("MainWindow", "جستجو"))
        self.ui.btn_browse_jpg_png_save.setText(_translate("MainWindow", "جستجو"))
        self.ui.save_label_jpg_png.setText(_translate("MainWindow", ": ذخیره در "))
        self.ui.fileaddress_label_jpg_png_2.setText(_translate("MainWindow", ": آدرس فایل "))
        self.ui.name_label_jpg_png.setText(_translate("MainWindow", ": اسم"))
        self.ui.label_jpg_png.setText(_translate("MainWindow", "تبدیل Jpg to Png"))
        self.ui.btn_clear_jpg_png.setText(_translate("MainWindow", "پاک کردن"))
        self.ui.btn_convert_jpg_png.setText(_translate("MainWindow", "تبدیل کردن"))
        self.ui.save_label_png_jpg.setText(_translate("MainWindow", ": ذخیره در "))
        self.ui.fileaddress_label_png_jpg.setText(_translate("MainWindow", ": آدرس فایل "))
        self.ui.btn_browse_png_jpg_address.setText(_translate("MainWindow", "جستجو"))
        self.ui.name_label_png_jpg.setText(_translate("MainWindow", ": اسم"))
        self.ui.btn_clear_png_jpg.setText(_translate("MainWindow", "پاک کردن"))
        self.ui.btn_convert_png_jpg.setText(_translate("MainWindow", "تبدیل کردن"))
        self.ui.btn_browse_png_jpg_save.setText(_translate("MainWindow", "جستجو"))
        self.ui.label_png_jpg.setText(_translate("MainWindow", "تبدیل Png to Jpg"))
        self.ui.label_setting.setText(_translate("MainWindow", "تنظیمات"))
        self.ui.label_info.setText(_translate("MainWindow", "طراحی شده توسط : سجاد فانی\n"
                                                            "زبان : پایتون 3.9\n"
                                                            "آیدی تلگرام : sajad_fani@\n"
                                                            "ایمیل : faniam321@gmail.com\n"))
        self.ui.btn_info.setText(_translate("MainWindow", "اطلاعات"))
        self.ui.btn_theme.setText(_translate("MainWindow", "تم"))
        self.ui.theme_1.setToolTip(_translate("MainWindow", "تم ۱"))
        self.ui.theme_3.setToolTip(_translate("MainWindow", "تم ۳"))
        self.ui.theme_2.setToolTip(_translate("MainWindow", "تم ۲"))
        self.ui.theme_4.setToolTip(_translate("MainWindow", "تم ۴"))
        self.ui.theme_6.setToolTip(_translate("MainWindow", "تم ۶"))
        self.ui.theme_5.setToolTip(_translate("MainWindow", "تم ۵"))
        self.ui.btn_language.setText(_translate("MainWindow", "زبان"))
        self.ui.btn_home.setToolTip(_translate("MainWindow", "خانه"))

    def german_language(self):
        _translate = QCoreApplication.translate
        self.ui.home_label.setText(_translate("MainWindow", "willkommen"))
        self.ui.btn_mp4_mp3.setText(_translate("MainWindow", "MP4 zu MP3"))
        self.ui.btn_jpg_png.setText(_translate("MainWindow", "Jpg zu Png"))
        self.ui.btn_png_jpg.setText(_translate("MainWindow", "Png zu Jpg"))
        self.ui.btn_setting.setText(_translate("MainWindow", "Einstellung"))
        self.ui.fileaddress_label_mp4_mp3.setText(_translate("MainWindow", "Dateiadresse:"))
        self.ui.label_mp4_mp3.setText(_translate("MainWindow", "Konvertieren Sie MP4 in MP3"))
        self.ui.btn_browse_mp4_mp3_address.setText(_translate("MainWindow", "wählen"))
        self.ui.savefile_label_mp4_mp3.setText(_translate("MainWindow", "Speichern als:"))
        self.ui.btn_browse_mp4_mp3_save.setText(_translate("MainWindow", "wählen"))
        self.ui.name_label_mp4_mp3.setText(_translate("MainWindow", "Name  :"))
        self.ui.time_label_mp4_mp3_2.setText(_translate("MainWindow", "Zeit  :"))
        self.ui.size_label_mp4_mp3.setText(_translate("MainWindow", "Größe :"))
        self.ui.btn_mp4_mp3_convert.setText(_translate("MainWindow", "Konvertieren"))
        self.ui.btn_mp4_mp3_clear.setText(_translate("MainWindow", "Klar"))
        self.ui.newsize_label_mp4_mp3.setText(_translate("MainWindow", "Neue Größe:"))
        self.ui.btn_browse_jpg_png_address.setText(_translate("MainWindow", "wählen"))
        self.ui.btn_browse_jpg_png_save.setText(_translate("MainWindow", "wählen"))
        self.ui.save_label_jpg_png.setText(_translate("MainWindow", "Speichern als :"))
        self.ui.fileaddress_label_jpg_png_2.setText(_translate("MainWindow", "Dateiadresse:"))
        self.ui.name_label_jpg_png.setText(_translate("MainWindow", "Name  :"))
        self.ui.label_jpg_png.setText(_translate("MainWindow", "Konvertieren Sie Jpg in Png"))
        self.ui.btn_clear_jpg_png.setText(_translate("MainWindow", "Klar"))
        self.ui.btn_convert_jpg_png.setText(_translate("MainWindow", "Konvertieren"))
        self.ui.save_label_png_jpg.setText(_translate("MainWindow", "Speichern als:"))
        self.ui.fileaddress_label_png_jpg.setText(_translate("MainWindow", "Dateiadresse:"))
        self.ui.btn_browse_png_jpg_address.setText(_translate("MainWindow", "wählen"))
        self.ui.name_label_png_jpg.setText(_translate("MainWindow", "Name  :"))
        self.ui.btn_clear_png_jpg.setText(_translate("MainWindow", "Klar"))
        self.ui.btn_convert_png_jpg.setText(_translate("MainWindow", "Konvertieren"))
        self.ui.btn_browse_png_jpg_save.setText(_translate("MainWindow", "wählen"))
        self.ui.label_png_jpg.setText(_translate("MainWindow", "Konvertieren Sie Png in Jpg"))
        self.ui.label_setting.setText(_translate("MainWindow", "Einstellung"))
        self.ui.label_info.setText(_translate("MainWindow", "Powered by : Sajjad fani\n"
                                                            "Sprache: Python 3.9\n"
                                                            "Telegramm-ID: @sajad_fani\n"
                                                            "E-Mail: faniam321@gmail.com"))
        self.ui.btn_info.setText(_translate("MainWindow", "Die Info"))
        self.ui.btn_theme.setText(_translate("MainWindow", "Thema"))
        self.ui.theme_1.setToolTip(_translate("MainWindow", "Thema 1"))
        self.ui.theme_3.setToolTip(_translate("MainWindow", "Thema 3"))
        self.ui.theme_2.setToolTip(_translate("MainWindow", "Thema 2"))
        self.ui.theme_4.setToolTip(_translate("MainWindow", "Thema 4"))
        self.ui.theme_6.setToolTip(_translate("MainWindow", "Thema 6"))
        self.ui.theme_5.setToolTip(_translate("MainWindow", "Thema 5"))
        self.ui.btn_language.setText(_translate("MainWindow", "Sprache"))
        self.ui.btn_home.setToolTip(_translate("MainWindow", "Heim"))

    def russian_language(self):
        _translate = QCoreApplication.translate
        self.ui.home_label.setText(_translate("MainWindow", "Добро пожаловать"))
        self.ui.btn_mp4_mp3.setText(_translate("MainWindow", "Mp4 в Mp3"))
        self.ui.btn_jpg_png.setText(_translate("MainWindow", "Jpg в Png"))
        self.ui.btn_png_jpg.setText(_translate("MainWindow", "Png в Jpg"))
        self.ui.btn_setting.setText(_translate("MainWindow", "Параметр"))
        self.ui.fileaddress_label_mp4_mp3.setText(_translate("MainWindow", "Адрес файла:"))
        self.ui.label_mp4_mp3.setText(_translate("MainWindow", "Конвертировать Mp4 в Mp3"))
        self.ui.btn_browse_mp4_mp3_address.setText(_translate("MainWindow", "Выбирать"))
        self.ui.savefile_label_mp4_mp3.setText(_translate("MainWindow", "Сохранить как  :"))
        self.ui.btn_browse_mp4_mp3_save.setText(_translate("MainWindow", "Выбирать"))
        self.ui.name_label_mp4_mp3.setText(_translate("MainWindow", "Имя  :"))
        self.ui.time_label_mp4_mp3_2.setText(_translate("MainWindow", "Время  :"))
        self.ui.size_label_mp4_mp3.setText(_translate("MainWindow", "Размер  :"))
        self.ui.btn_mp4_mp3_convert.setText(_translate("MainWindow", "Перерабатывать"))
        self.ui.btn_mp4_mp3_clear.setText(_translate("MainWindow", "Прозрачный"))
        self.ui.newsize_label_mp4_mp3.setText(_translate("MainWindow", "Новый размер:"))
        self.ui.btn_browse_jpg_png_address.setText(_translate("MainWindow", "Выбирать"))
        self.ui.btn_browse_jpg_png_save.setText(_translate("MainWindow", "Выбирать"))
        self.ui.save_label_jpg_png.setText(_translate("MainWindow", "Сохранить как  :"))
        self.ui.fileaddress_label_jpg_png_2.setText(_translate("MainWindow", "Адрес файла:"))
        self.ui.name_label_jpg_png.setText(_translate("MainWindow", "Имя  :"))
        self.ui.label_jpg_png.setText(_translate("MainWindow", "Конвертировать Jpg в Png"))
        self.ui.btn_clear_jpg_png.setText(_translate("MainWindow", "Прозрачный"))
        self.ui.btn_convert_jpg_png.setText(_translate("MainWindow", "Перерабатывать"))
        self.ui.save_label_png_jpg.setText(_translate("MainWindow", "Сохранить как  :"))
        self.ui.fileaddress_label_png_jpg.setText(_translate("MainWindow", "Адрес файла:"))
        self.ui.btn_browse_png_jpg_address.setText(_translate("MainWindow", "Выбирать"))
        self.ui.name_label_png_jpg.setText(_translate("MainWindow", "Имя  :"))
        self.ui.btn_clear_png_jpg.setText(_translate("MainWindow", "Прозрачный"))
        self.ui.btn_convert_png_jpg.setText(_translate("MainWindow", "Перерабатывать"))
        self.ui.btn_browse_png_jpg_save.setText(_translate("MainWindow", "Выбирать"))
        self.ui.label_png_jpg.setText(_translate("MainWindow", "Конвертировать Png в Jpg"))
        self.ui.label_setting.setText(_translate("MainWindow", "Параметр"))
        self.ui.label_info.setText(_translate("MainWindow", "Powered by : Sajjad fani\n"
                                                            "Language : Python 3.9\n"
                                                            "Telegram ID : @sajad_fani\n"
                                                            "Email : faniam321@gmail.com"))
        self.ui.btn_info.setText(_translate("MainWindow", "Информация"))
        self.ui.btn_theme.setText(_translate("MainWindow", "Тема"))
        self.ui.theme_1.setToolTip(_translate("MainWindow", "Тема 1"))
        self.ui.theme_3.setToolTip(_translate("MainWindow", "Тема 3"))
        self.ui.theme_2.setToolTip(_translate("MainWindow", "Тема 2"))
        self.ui.theme_4.setToolTip(_translate("MainWindow", "Тема 4"))
        self.ui.theme_6.setToolTip(_translate("MainWindow", "Тема 6"))
        self.ui.theme_5.setToolTip(_translate("MainWindow", "Тема 5"))
        self.ui.btn_language.setText(_translate("MainWindow", "Язык"))
        self.ui.btn_home.setToolTip(_translate("MainWindow", "Дом"))


def setup():
    app = QApplication([])
    ui = Convertor()
    ui.show()
    app.exec_()


setup()
