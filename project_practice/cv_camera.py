import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from ui_mainwindow import Ui_MainWindow
import bank_and_face


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.filename = 'result/1.jpg'
        self.filename2 = 'result/2.jpg'
        self.camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.is_camera_opened = False  # 摄像头有没有打开标记

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.label.setText('关闭摄像头')
            self._timer.start()
        else:
            self.label.setText('打开摄像头')
            self._timer.stop()

    def btnCapture_Clicked(self):
        '''
        捕获图片,此位置保存图片，下面传到face++
        '''
        # 摄像头未打开，不执行任何操作
        if not self.is_camera_opened:
            return

        self.captured = self.frame
        print(self.frame)
        cv2.imwrite(self.filename, self.frame)
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnReadImage_Clicked(self):
        '''
        从本地读取图片 文件路径不能有中文
        '''
        # 打开文件选取对话框
        filename, _ = QFileDialog.getOpenFileName(self, '打开图片')
        if filename:
            self.captured = cv2.imread(str(filename))
            cv2.imwrite(self.filename, self.captured)
            print(self.captured)
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)

            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnGray_Clicked(self):

        # 如果没有捕获图片，则不执行操作
        # if not hasattr(self,"captured"):
            # return
        # self.img = self.captured
        try:
            bank_card = bank_and_face.card_recognition(self.filename)
            img = bank_and_face.faces[bank_card]
            name = bank_and_face.informations[img][0]
            person_number = bank_and_face.informations[img][1]
            self.information_name.setText(name)
            self.information_num.setText(person_number)
            img = bank_and_face.person_beauty(img)
            cv2.imwrite(self.filename2, img)
            self.captured = cv2.imread(str(self.filename2))
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)
            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            self.labelResult.setText("请重试")



    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片'''
        ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)

        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine,QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())