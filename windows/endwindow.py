# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'endwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_End_window(object):
    def setupUi(self, End_window):
        End_window.setObjectName("End_window")
        End_window.resize(400, 300)
        self.end_label = QtWidgets.QLabel(End_window)
        self.end_label.setGeometry(QtCore.QRect(150, 70, 71, 31))
        self.end_label.setObjectName("end_label")
        self.again_button = QtWidgets.QPushButton(End_window)
        self.again_button.setGeometry(QtCore.QRect(100, 160, 181, 101))
        self.again_button.setObjectName("again_button")

        self.retranslateUi(End_window)
        QtCore.QMetaObject.connectSlotsByName(End_window)

    def retranslateUi(self, End_window):
        _translate = QtCore.QCoreApplication.translate
        End_window.setWindowTitle(_translate("End_window", "END"))
        self.end_label.setText(_translate("End_window", "TextLabel"))
        self.again_button.setText(_translate("End_window", "再来一把"))
