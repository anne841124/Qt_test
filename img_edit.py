import cv2
import sys
import numpy as np
from PySide6.QtWidgets import QPushButton, QDialog, QLabel, QGridLayout, QApplication, QFileDialog, QComboBox, QLineEdit
from PySide6.QtCore import *
from PySide6.QtGui import QImage, QPixmap

class pic_edit(QDialog):
    def __init__(self):
        self.img = np.ndarray(()) # 初始化 img 用以儲存圖片
        super(pic_edit, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.Open_btn = QPushButton('Open', self)
        self.Save_btn = QPushButton('Save', self)
        self.Blur_btn = QPushButton('Blur', self)
        self.Rotate_btn = QPushButton('Rotate', self)
        self.Blur_com = QComboBox()
        self.Blur_com.addItem("blur")
        self.Blur_com.addItem("MedianBlur")
        self.Blur_com.addItem("GaussianBlur")
        self.Kernel_edit = QLineEdit()
        self.Quit_btn = QPushButton('Quit', self)
        self.label = QLabel()

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 5)
        layout.addWidget(self.Open_btn, 4, 1, 1, 1)
        layout.addWidget(self.Rotate_btn, 4, 2, 1, 1)
        layout.addWidget(self.Save_btn, 4, 3, 1, 1)
        layout.addWidget(self.Blur_btn, 5, 4, 1, 1)
        layout.addWidget(self.Blur_com, 5, 1, 1, 2)
        layout.addWidget(self.Kernel_edit, 5, 3, 1, 1)
        layout.addWidget(self.Quit_btn, 4, 4, 1, 1)

        self.Open_btn.clicked.connect(self.Open_img)
        self.Save_btn.clicked.connect(self.Save_img)
        self.Blur_btn.clicked.connect(self.Blur_img)
        self.Rotate_btn.clicked.connect(self.Rotate_img)
        self.Quit_btn.clicked.connect(self.close)

    def Open_img(self):
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '* .png * .jpg * .bmp')
        if fileName == '':
            return
        self.img = cv2.imread(fileName, -1)
        if self.img.size == 1:
            return
        self.show_img()

    def Save_img(self):
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '* .png * .jpg * .bmp')
        if fileName == '':
            return
        if self.img.size == 1:
            return
        print(fileName)
        cv2.imwrite(fileName + '.jpg', self.img)

    def Blur_img(self):
        ker_size = int(self.Kernel_edit.text())
        
        if self.img.size == 1:
            return
        if self.Blur_com.currentText() == 'blur':
            self.img = cv2.blur(self.img, (ker_size, ker_size))
            self.show_img()

        elif self.Blur_com.currentText() == 'MedianBlur':
            self.img = cv2.medianBlur(self.img, ker_size)
            self.show_img()
        
        elif self.Blur_com.currentText() == 'GaussianBlur':
            self.img = cv2.GaussianBlur(self.img, (ker_size, ker_size), 0)
            self.show_img()

    def Rotate_img(self):
        height = self.img.shape[0]
        width  = self.img.shape[1]
        center = (int(height/2), int(width/2))

        angle = 90.0
        scale = 1.0

        trans = cv2.getRotationMatrix2D(center, angle, scale)
        self.img = cv2.warpAffine(self.img, trans, (width, height))
        self.show_img()

    def show_img(self):
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.Qimg = QImage(self.img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(self.Qimg))

if __name__ == '__main__':
    app = QApplication()
    edit = pic_edit()
    edit.show()
    sys.exit(app.exec())