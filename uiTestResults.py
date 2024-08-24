# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\TestResultsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(865, 403)
        self.layoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_6.setGeometry(QtCore.QRect(10, 10, 411, 381))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayoutTrainFig1 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayoutTrainFig1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutTrainFig1.setObjectName("verticalLayoutTrainFig1")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(430, 10, 271, 381))
        self.tableWidget.setRowCount(12)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(70)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Test Results"))

