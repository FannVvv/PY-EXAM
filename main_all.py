# coding:utf-8
from windows.mainwindow import *
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow, Ui_mainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.open_second()

    def open_second(self):
        self.pushButton_2.clicked.connect(second_window.show)
        self.close()


class second_window(QMainWindow, Ui_mainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class end_window(QMainWindow, Ui_mainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()  # 实例化主窗口
    second_window = second_window()  # 实例化第二个窗口
    end_window = end_window()  # 实例化结束窗口
    main_window.show()
    sys.exit(app.exec_())
