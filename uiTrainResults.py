# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\TrainResultsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(421, 381)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 403, 363))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutTrainFig3 = QtWidgets.QVBoxLayout()
        self.verticalLayoutTrainFig3.setObjectName("verticalLayoutTrainFig3")
        self.gridLayout.addLayout(self.verticalLayoutTrainFig3, 1, 0, 1, 1)
        self.verticalLayoutTrainFig1 = QtWidgets.QVBoxLayout()
        self.verticalLayoutTrainFig1.setObjectName("verticalLayoutTrainFig1")
        self.gridLayout.addLayout(self.verticalLayoutTrainFig1, 0, 0, 1, 1)
        self.verticalLayoutTrainFig4 = QtWidgets.QVBoxLayout()
        self.verticalLayoutTrainFig4.setObjectName("verticalLayoutTrainFig4")
        self.gridLayout.addLayout(self.verticalLayoutTrainFig4, 1, 1, 1, 1)
        self.verticalLayoutTrainFig2 = QtWidgets.QVBoxLayout()
        self.verticalLayoutTrainFig2.setObjectName("verticalLayoutTrainFig2")
        self.gridLayout.addLayout(self.verticalLayoutTrainFig2, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Train Results"))

