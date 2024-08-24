# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\ValidResultsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(274, 179)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutTrainFig1 = QtWidgets.QVBoxLayout()
        self.verticalLayoutTrainFig1.setObjectName("verticalLayoutTrainFig1")
        self.horizontalLayout.addLayout(self.verticalLayoutTrainFig1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidgetData = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidgetData.setAlternatingRowColors(True)
        self.tableWidgetData.setRowCount(0)
        self.tableWidgetData.setColumnCount(2)
        self.tableWidgetData.setObjectName("tableWidgetData")
        self.tableWidgetData.horizontalHeader().setVisible(False)
        self.tableWidgetData.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidgetData.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidgetData.horizontalHeader().setMinimumSectionSize(70)
        self.tableWidgetData.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_2.addWidget(self.tableWidgetData)
        self.horizontalLayout.addWidget(self.groupBox)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Valid Results"))
        self.groupBox.setTitle(_translate("Dialog", "Validataion Data: Experiment vs Prediction"))

