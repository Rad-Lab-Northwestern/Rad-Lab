import sys
import  os
from time import sleep

"""
    AI import
"""
# import tesnsorflow.keras as keras
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
# from tensorflow.keras.layers import Dense
# from tensorflow.keras import activations
# from tensorflow.keras import losses
# from tensorflow.keras import optimizers
# from tensorflow.keras import metrics
# from tensorflow.keras import backend as K
# from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
# import numpy as np
# import seaborn as sns
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,KFold
import pandas as pd
"""
    matplotlib import
"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
"""
    Qt import
"""
from PyQt5 import QtCore, QtGui, QtWidgets,uic
import PyQt5
from PyQt5.QtWidgets import QApplication,QStyle,QMessageBox,QFileDialog,QVBoxLayout,QFrame,QTableWidgetItem
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QByteArray,QEvent,QObject,QPoint,QSysInfo,QFileInfo
from PyQt5.QtGui import QPixmap

"""
    UI import
"""
import uiMain


"""
    MainApp Class
"""

ModelPath=".\\Models"

class MyCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MyCanvas, self).__init__(fig)


class mainApp(QtWidgets.QDialog,uiMain.Ui_Dialog):
    def __init__(self,parent=None):
        super(mainApp,self).__init__(parent)
        self.setupUi(self)
        self.dataset=None

        h5fileslist=[f for f in os.listdir(ModelPath) if os.path.isfile(os.path.join(ModelPath,f)) and f.endswith('.h5')]
        h5fileslist.insert(0,'---')

        self.comboBoxModels.clear()
        for file in h5fileslist:
            self.comboBoxModels.addItem(file)
        self.comboBoxModels.setCurrentIndex(1)

        sc = MyCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.verticalLayoutFigure.addWidget(sc)
        # header=QtWidgets.QHeaderView(QtCore.Qt.Horizontal)
        # header.setProperty('stretchLastSection')
        # self.tableViewData.setHorizontalHeader(header)
        # self.tableViewData.resizeColumnsToContents()
        
        self.tableWidgetData.setHorizontalHeaderLabels(["Time(s)", "Temperature"])

        if QSysInfo.productType() == "windows" and QSysInfo.productVersion() == "10":
            self.setStyleSheet(
                "QHeaderView::section{"
                    "border-top:0px solid #D8D8D8;"
                    "border-left:0px solid #D8D8D8;"
                    "border-right:1px solid #D8D8D8;"
                    "border-bottom: 1px solid #D8D8D8;"
                    "background-color:white;"
                    "padding:4px;"
                "}"
                "QTableCornerButton::section{"
                    "border-top:0px solid #D8D8D8;"
                    "border-left:0px solid #D8D8D8;"
                    "border-right:1px solid #D8D8D8;"
                    "border-bottom: 1px solid #D8D8D8;"
                    "background-color:white;"
                "}"
            )
        # self.lcdNumberPredictedTemperature.display('{:.01f}'.format(999.9))
        self.lcdNumberPredictedTemperature.display('---.-')
        self.on_radioButtonDataUpload_toggled()
        self.labelDataFileName.setText('')
        self.labelModelFileName.setText('')

        # self.show()

    @QtCore.pyqtSlot()
    def on_pushButtonPredict_clicked(self):

        if self.radioButtonDataTable.isChecked():
            print(self.tableWidgetData.rowCount())
            print(self.tableWidgetData.columnCount())
            for row in range(self.tableWidgetData.rowCount()):
                item0=self.tableWidgetData.item(row,0)
                item1=self.tableWidgetData.item(row,1)
                if(item0):
                    print(int(item0.text()))
                if(item1):
                    print(int(item1.text()))

    def on_comboBoxModels_currentIndexChanged(self,index):
        if(index==0):
            # self.on_pushButtonLoadModel_clicked()
            pass
        else:
            self.labelModelFileName.setText('')

    @QtCore.pyqtSlot()
    def on_pushButtonLoadModel_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Load h5 Model", 
                                                  ModelPath,"h5 Files (*.h5)",
                                                    options=options
                                                    )
        if(fileName):
            self.comboBoxModels.setCurrentIndex(0)
            self.labelModelFileName.setText(QFileInfo(fileName).fileName())

    def  on_tableWidgetData_cellPressed(self,row,column):
        # print(row,column)
        item=self.tableWidgetData.item(row,column)
        # if(item):
        #    print(item.text())

    def on_radioButtonDataUpload_toggled(self):
        self.pushButtonLoadData.setEnabled(self.radioButtonDataUpload.isChecked())
        if(self.radioButtonDataUpload.isChecked()):
            for row in range(self.tableWidgetData.rowCount()):
                item0=self.tableWidgetData.item(row,0)
                item1=self.tableWidgetData.item(row,1)
                if(item0):
                    item0.setFlags(item0.flags() ^ QtCore.Qt.ItemIsEditable)
                if(item1):
                    item1.setFlags(item1.flags() ^ QtCore.Qt.ItemIsEditable)

    def on_radioButtonDataTable_toggled(self):
        if(self.radioButtonDataTable.isChecked()):
            self.labelDataFileName.setText('')
            for row in range(self.tableWidgetData.rowCount()):
                item0=self.tableWidgetData.item(row,0)
                item1=self.tableWidgetData.item(row,1)
                if(item0):
                    item0.setFlags(item0.flags() | QtCore.Qt.ItemIsEditable)
                if(item1):
                    item1.setFlags(item1.flags() | QtCore.Qt.ItemIsEditable)

    @QtCore.pyqtSlot()
    def on_pushButtonLoadData_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Load Data", 
                                                  "","CsV Files (*.csv)",
                                                    options=options
                                                    )
        if(fileName):
            # print(fileName)
            self.labelDataFileName.setText(QFileInfo(fileName).fileName())
            self.dataset=pd.read_csv(fileName,header=None)
            dataset=self.dataset.reset_index()
            for index,row in  dataset.iterrows() :
                # print(index,row[0],row[1])
                c0=QTableWidgetItem(str(row[0]))
                c1=QTableWidgetItem(str(row[1]))
                c0.setFlags(c0.flags() ^ QtCore.Qt.ItemIsEditable)
                c1.setFlags(c1.flags() ^ QtCore.Qt.ItemIsEditable)
                self.tableWidgetData.setItem(index,0,c0)
                self.tableWidgetData.setItem(index,1,c1)
            

def main():
    # df = pd.DataFrame([[1,2,3],[4,5,6]])
    # df = pd.DataFrame([*zip([1,2,3],[4,5,6])])
    # print(df)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"]="1"
    if hasattr(QtCore.Qt,'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,True)
    if hasattr(QtCore.Qt,'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,True)    
    app=QApplication(sys.argv)
    form=mainApp()
    form.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
    form.show()
    app.exec()

if __name__=="__main__":
    main()