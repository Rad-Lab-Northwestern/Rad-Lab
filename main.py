import sys
import  os
from time import sleep

"""
    AI import
"""
import keras
# import tesnsorflow.keras as keras
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
from keras.models import load_model
# from tensorflow.keras.layers import Dense
# from tensorflow.keras import activations
from keras import losses
from keras import optimizers
# from tensorflow.keras import metrics
# from keras import backend as K
from keras import initializers
# from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
import numpy as np
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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
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
import math
import uiMain
import uiFig

"""
    MainApp Class
"""

ModelPath=".\\Models"
"""
    Canvas Class
"""
class MyCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MyCanvas, self).__init__(self.fig)

"""
    FigureUi Form Class
"""
class FigUi(QtWidgets.QDialog,uiFig.Ui_Dialog):
    def __init__(self):
        super(FigUi,self).__init__()
        self.setupUi(self)

    def showFig(self,sc,index):
        if(index==0):
            while self.verticalLayoutTrainFig1.count()!=0:
                for i in range(self.verticalLayoutTrainFig1.count()):
                   self.verticalLayoutTrainFig1.takeAt(i)

            self.toolbar1 = NavigationToolbar(sc, self)
            self.verticalLayoutTrainFig1.addWidget(self.toolbar1)
            self.verticalLayoutTrainFig1.addWidget(sc)
            self.verticalLayoutTrainFig1.setAlignment(Qt.AlignCenter )
        else:
            while self.verticalLayoutTrainFig2.count()!=0:
                for i in range(self.verticalLayoutTrainFig2.count()):
                   self.verticalLayoutTrainFig2.takeAt(i)
            self.toolbar2 = NavigationToolbar(sc, self)
            self.verticalLayoutTrainFig2.addWidget(self.toolbar2)
            self.verticalLayoutTrainFig2.addWidget(sc)
            self.verticalLayoutTrainFig2.setAlignment(Qt.AlignCenter )
"""
    keras Callbacks
"""
class CustomCallback(keras.callbacks.Callback):
    def __init__(self,progressbar,maxepoch):
        self.maxepoch=maxepoch
        self.progress=progressbar
    def round(x):
        return int(math.floor(x+0.5))
            
    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())
        # print("End epoch {} of training; got log keys: {}".format(epoch, keys))
        self.progress.setValue(round(float((epoch+1)/self.maxepoch)*100))

""""
    MainUi Class
"""
class mainApp(QtWidgets.QDialog,uiMain.Ui_Dialog):
    def __init__(self,parent=None):
        super(mainApp,self).__init__(parent)
        self.setupUi(self)
        self.PredictDataset=None
        self.PredictModeladdress=''
        self.PredictDataaddress=''

        self.TrainDataset=None
        self.TrainDataaddress=''
        self.TrainModeladdress=''        
        self.TraincurrentModel=None
        self.formFig=FigUi()
        

        h5fileslist=[f for f in os.listdir(ModelPath) if os.path.isfile(os.path.join(ModelPath,f)) and f.endswith('.h5')]
        h5fileslist.insert(0,'---')
        self.comboBoxModels.clear()
        for file in h5fileslist:
            self.comboBoxModels.addItem(file)
            self.comboBoxTrainModels.addItem(file)
        self.comboBoxModels.setCurrentIndex(1)
        self.comboBoxTrainModels.setCurrentIndex(1)

        self.comboBoxModels.currentIndexChanged.connect(self.on_comboBoxModels_indexchanged)
        self.comboBoxTrainModels.currentIndexChanged.connect(self.on_comboBoxModels_indexchanged)
        self.pushButtonTrainLoadModel.clicked.connect(self.on_pushButtonLoadModel_clicked)     


        self.labelModelFileName.setText('')
        self.PredictModeladdress=os.path.join(ModelPath,
                                        self.comboBoxModels.currentText()
                                        )     
        self.TrainModeladdress=self.PredictModeladdress
             
        self.sc1=None


        # sc = MyCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # self.verticalLayoutTrainFig1.addWidget(sc)


        self.tableWidgetData.setHorizontalHeader(QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal))
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
        
        self.lcdNumberPredictedTemperature.setStyleSheet(
            "QLCDNumber{"
            "color:rgb(0, 208, 0);"
            # "background-color:rgb(0, 170, 255);"
            "}"
        )
        self.lcdNumberPredictedTemperature.display('---.--')
        self.on_radioButtonDataUpload_toggled()
        self.labelDataFileName.setText('')
        self.labelModelFileName.setText('')
        self.pushButtonLoadData.setEnabled(False)
        self.pushButtonTrainLoadData.setEnabled(False)
        self.pushButtonTrain.setEnabled(False)
        self.pushButtonTrainSaveModel.setEnabled(False)

    """
                handle widgets of Predict
    """        
        
    def on_tabWidget_currentChanged (slef ,index) :
        print('currentindexchanged')

    def on_comboBoxModels_indexchanged(self,index):
        print(index)
        if(index==0):
            #self.on_pushButtonLoadModel_clicked()
            pass
        else:
            self.labelModelFileName.setText('')
            self.PredictModeladdress=os.path.join(ModelPath,
                                           self.comboBoxModels.currentText()
                                           )
    
    @QtCore.pyqtSlot()
    def on_pushButtonLoadModel_clicked(self):
        print('load model')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Load h5 Model", 
                                                  ModelPath,"h5 Files (*.h5)",
                                                    options=options
                                                    )
        if(fileName):
            self.comboBoxModels.setCurrentIndex(0)
            self.comboBoxTrainModels.setCurrentIndex(0)
            self.labelModelFileName.setText(QFileInfo(fileName).fileName())
            self.labelTrainModelFileName.setText(QFileInfo(fileName).fileName())

            self.PredictModeladdress=fileName
            self.TrainModeladdress=fileName

            print(self.PredictModeladdress)

    def on_radioButtonDataUpload_toggled(self):
        self.pushButtonLoadData.setEnabled(self.radioButtonDataUpload.isChecked())
        self.checkBoxWithHeader.setEnabled(self.radioButtonDataUpload.isChecked())
        self.pushButtonLoadData.setEnabled(False)
        if(self.radioButtonDataUpload.isChecked()):
            for row in range(self.tableWidgetData.rowCount()):
                item0=self.tableWidgetData.item(row,0)
                item1=self.tableWidgetData.item(row,1)
                if(item0):
                    item0.setFlags(item0.flags() ^ QtCore.Qt.ItemIsEditable)
                if(item1):
                    item1.setFlags(item1.flags() ^ QtCore.Qt.ItemIsEditable)

    def on_radioButtonDataTable_toggled(self):
        self.pushButtonLoadData.setEnabled(False)
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
    def on_pushButtonLoadDataFile_clicked(self):
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
            self.PredictDataaddress=fileName
            self.pushButtonLoadData.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_pushButtonLoadData_clicked(self):
        if(self.checkBoxWithHeader.isChecked()):
            self.PredictDataset=pd.read_csv(self.PredictDataaddress)
        else:
            self.PredictDataset=pd.read_csv(self.PredictDataaddress,header=None)

        dataset=self.PredictDataset.reset_index()
        r=0
        for index,row in  dataset.iterrows() :
            if(index==0 and self.checkBoxWithHeader.isChecked()):
                pass
            else:
                c0=QTableWidgetItem(str(row[0]))
                c1=QTableWidgetItem(str(row[1]))
                c0.setFlags(c0.flags() ^ QtCore.Qt.ItemIsEditable)
                c1.setFlags(c1.flags() ^ QtCore.Qt.ItemIsEditable)
                self.tableWidgetData.setItem(r,0,c0)
                self.tableWidgetData.setItem(r,1,c1)
                r+=1

    def  on_tableWidgetData_cellPressed(self,row,column):
        print(row,column)
        item=self.tableWidgetData.item(row,column)
        # if(item):
        #    print(item.text())

    @QtCore.pyqtSlot()
    def on_pushButtonPredict_clicked(self):
        if self.radioButtonDataTable.isChecked():
            time=[]
            temperature=[]
            for row in range(self.tableWidgetData.rowCount()):
                item0=self.tableWidgetData.item(row,0)
                item1=self.tableWidgetData.item(row,1)

                print('row={row}'.format(row=row))

                if(item0 and item0.text()!=''):
                    pass
                else:
                    item = QTableWidgetItem()
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    item.setText('0')
                    self.tableWidgetData.setItem(row,0,item)
                    item0=self.tableWidgetData.item(row,0)

                if(item1 and item1.text()!=''):
                    pass
                else:
                    item = QTableWidgetItem()
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    item.setText('0')
                    self.tableWidgetData.setItem(row,1,item)
                    item1=self.tableWidgetData.item(row,1)  
                
                time.append(float(item0.text()))
                temperature.append(float(item1.text()))
            self.PredictDataset=pd.DataFrame([*zip(time,temperature)])
        model=load_model(self.PredictModeladdress)
        print(model.summary())
        data_x=self.PredictDataset.iloc[:,1].values.astype('float')
        data_x=np.reshape(data_x,(1,11))
        result=model.predict(data_x)
        print(result[0])
        self.lcdNumberPredictedTemperature.display('{:.02f}'.format(result[0][0]))

    """
                handle widgets of Train
    """   
    @QtCore.pyqtSlot()
    def on_pushButtonTrainSaveModel_clicked(self):
        print('save model')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog. getSaveFileName(self,
                                                  "Save h5 Model", 
                                                  ModelPath,"h5 Files (*.h5)",
                                                    options=options
                                                    )
        if(fileName):
            if(not fileName.endswith('.h5')):
                fileName=fileName+'.h5'
            print(fileName)
            self.TraincurrentModel.save(fileName)
            self.comboBoxModels.setCurrentIndex(0)
            self.comboBoxTrainModels.setCurrentIndex(0)
            self.labelModelFileName.setText(QFileInfo(fileName).fileName())
            self.labelTrainModelFileName.setText(QFileInfo(fileName).fileName())   
            self.PredictModeladdress=fileName
            self.TrainModeladdress=fileName                     

    @QtCore.pyqtSlot()
    def on_pushButtonTrainLoadDataFile_clicked(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Load Data", 
                                                  "","CsV Files (*.csv)",
                                                    options=options
                                                    )
        if(fileName):
            # print(fileName)
            self.labelTrainDataFileName.setText(QFileInfo(fileName).fileName())
            self.TrainDataaddress=fileName
            self.pushButtonTrainLoadData.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_pushButtonTrainLoadData_clicked(self):
        print('clicked load data')
        if(self.checkBoxTrainWithHeader.isChecked()):
            self.TrainDataset=pd.read_csv(self.TrainDataaddress)
            data=self.TrainDataset.iloc[1:,:]
        else:
            self.TrainDataset=pd.read_csv(self.TrainDataaddress,header=None)   
            data=self.TrainDataset.iloc[:,:]
     
        sc1=MyCanvas(self, width=5, height=4, dpi=80)
        t= np.linspace(0,150,302)
        for i in range(len(data)):
            sc1.axes.plot(t,data.iloc[i,:])
        sc1.axes.axvline(x=5,color='black',ls='--')        
        sc1.axes.set_title("loaded Data", fontsize=8)
        sc1.axes.set_xlabel('time (s)', fontsize=8)
        sc1.axes.set_ylabel('Maximum Temperature $(^OC)$"', fontsize=8)
        sc1.axes.tick_params(axis='both', which='major',labelsize=8)
        sc1.axes.grid(True)
        self.formFig.showFig(sc1,0)
        self.formFig.show()
        self.pushButtonTrain.setEnabled(True)     

    def reset_weights(self,model):
        # session = K.get_session()
        for layer in model.layers: 
            print(layer)
            if hasattr(layer, 'kernel_initializer'):
                print('init kernel')
                # layer.kernel.initializer(initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None))
                # layer.kernel.initializer.run(session=session)

    @QtCore.pyqtSlot()
    def on_pushButtonTrain_clicked(self):
        self.TraincurrentModel=load_model(self.TrainModeladdress)
        print(self.TraincurrentModel.summary())
        
        if(self.checkBoxTrainWithHeader.isChecked()):
            data=self.TrainDataset.iloc[1:,:]
        else:
            data=self.TrainDataset.iloc[:,:]

        data_x=data.iloc[:,0:11].values.astype('float')
        data_y=data.iloc[:,-1].values.astype('float')
        if(self.checkBoxTrainReinitWeights.isChecked()):
            self.reset_weights(self.TraincurrentModel)
            opt=optimizers.Adam(self.doubleSpinBoxTrainLearningRate.value())
            self.TraincurrentModel.compile(loss='mse',optimizer=opt,metrics=['mse'])        
        history = self.TraincurrentModel.fit(data_x, data_y, 
                                             epochs=self.spinBoxTrainEpochNum.value(), 
                                             validation_split=self.doubleSpinBoxTrainValidationSplit.value()/100.0,
                                             batch_size=self.spinBoxTrainBatchSize.value(),
                                             verbose=0,
                                            callbacks=[CustomCallback(self.progressBarTrain,self.spinBoxTrainEpochNum.value())])
        
        sc2=MyCanvas(self, width=5, height=4, dpi=100)        
        sc2.axes.plot(history.history['loss'])
        sc2.axes.plot(history.history['val_loss'])
        sc2.axes.legend(['Training Loss', 'Validation Loss'], fontsize=8)
        sc2.axes.set_title("Training Loss", fontsize=8)
        sc2.axes.set_xlabel('Epoch', fontsize=8)
        sc2.axes.set_ylabel('Loss', fontsize=8)
        sc2.axes.tick_params(axis='both', which='major',labelsize=8)
        sc2.axes.grid(True)
        self.formFig.showFig(sc2,1)
        self.formFig.show()
        self.pushButtonTrainSaveModel.setEnabled(True)


    def closeEvent(self,event):
        print("closing app")
        self.formFig.close()
        event.accept()

      
"""
    Star Main code
"""
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