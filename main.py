import sys
import  os
from time import sleep

"""
    AI import
"""
import tensorflow.keras as keras
# import keras

# from tensorflow.keras.models import Sequential

from tensorflow.keras.models import load_model
# from keras.models import load_model #python>3.6

# from tensorflow.keras.layers import Dense
# from tensorflow.keras import activations

from tensorflow.keras import losses
# from keras import losses  #python>3.6

from tensorflow.keras import optimizers
# from keras import optimizers  #python>3.6

# from tensorflow.keras import metrics
# from keras import backend as K

from tensorflow.keras import initializers
# from keras import initializers    #python>3.6

# from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
import numpy as np
# import seaborn as sns
import sklearn
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,KFold
import pandas as pd

print(keras.__version__)
print(sklearn.__version__)
print(pd.__version__)
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
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QByteArray,QEvent,QObject,QPoint,QSysInfo,QFileInfo,QSize
from PyQt5.QtGui import QPixmap

"""
    UI import
"""
import math
import uiMain
import uiTrainResults
import  uiValidResults
"""
    MainApp Class
"""

ModelPath=".\\Models"
"""
    Canvas Class
"""
class MyCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, row=1,column=1, dpi=70):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.subplots(row,column) #fig.add_subplot(111)
        super(MyCanvas, self).__init__(self.fig)
"""
    uiTestResults Class
"""
class formValidUi(QtWidgets.QDialog,uiValidResults.Ui_Dialog):
    def __init__(self):
        super(formValidUi,self).__init__()
        self.setupUi(self)

        screen=app.desktop().geometry()
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                        Qt.AlignLeft|Qt.AlignVCenter,
                                        QSize(int(np.ceil(screen.width()*0.5)),int(np.ceil(screen.height()*0.6))),
                                        app.primaryScreen().availableGeometry()
                                        )
                        )
        self.tableWidgetData.setHorizontalHeader(QtWidgets.QHeaderView(QtCore.Qt.Horizontal))
        # self.tableWidgetData.setHorizontalHeader(QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)) #python>3.6
        self.tableWidgetData.setHorizontalHeaderLabels([r"Experiment('C)", r"Predict('C)"])
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

        self.canvas1=MyCanvas(self)

        self.toolbar1 = NavigationToolbar(self.canvas1,self)
        self.verticalLayoutValidFig1.addWidget(self.toolbar1)
        self.verticalLayoutValidFig1.addWidget(self.canvas1)
        self.verticalLayoutValidFig1.setAlignment(Qt.AlignCenter ) 


    def fillTable(self,data_C0,data_C1):
        print(len(data_C0))
        for r in range(self.tableWidgetData.rowCount()):
            self.tableWidgetData.removeRow(r)
            
        for r in range(len(data_C0)):

            c0=QTableWidgetItem(str(data_C0[r]))
            c1=QTableWidgetItem(str(data_C1[r][0]))
            c0.setFlags(c0.flags() ^ QtCore.Qt.ItemIsEditable)
            c1.setFlags(c1.flags() ^ QtCore.Qt.ItemIsEditable)
            currentIndex=self.tableWidgetData.rowCount()
            self.tableWidgetData.setRowCount(currentIndex+1)
            self.tableWidgetData.setItem(r,0,c0)
            self.tableWidgetData.setItem(r,1,c1)
        self.tableWidgetData.setVisible(False)
        self.tableWidgetData.resizeColumnsToContents()
        self.tableWidgetData.setVisible(True)            

    def getaxes(self,index):
        if(index==1):
            self.canvas1.fig.axes[0].clear()
            return self.canvas1.fig.axes[0]
         
    def show(self,index):
        if(index==1):
            self.canvas1.draw_idle()
        super().show()

"""
    uiTrainResults Class
"""
class formTrainUi(QtWidgets.QDialog,uiTrainResults.Ui_Dialog):
    def __init__(self):
        super(formTrainUi,self).__init__()
        self.setupUi(self)

        screen=app.desktop().geometry()
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                        Qt.AlignRight|Qt.AlignVCenter,
                                        QSize(int(np.ceil(screen.width()*0.6)),int(np.ceil(screen.height()*0.87))),
                                        app.primaryScreen().availableGeometry()
                                        )
                        ) 
                  
        self.canvas1=MyCanvas(self)
        self.canvas2=MyCanvas(self)
        self.canvas3=MyCanvas(self)
        self.canvas4=MyCanvas(self)

        self.toolbar1 = NavigationToolbar(self.canvas1,self)
        self.verticalLayoutTrainFig1.addWidget(self.toolbar1)
        self.verticalLayoutTrainFig1.addWidget(self.canvas1)
        self.verticalLayoutTrainFig1.setAlignment(Qt.AlignCenter ) 

        self.toolbar2 = NavigationToolbar(self.canvas2,self)
        self.verticalLayoutTrainFig2.addWidget(self.toolbar2)
        self.verticalLayoutTrainFig2.addWidget(self.canvas2)
        self.verticalLayoutTrainFig2.setAlignment(Qt.AlignCenter ) 

        self.toolbar3 = NavigationToolbar(self.canvas3,self)
        self.verticalLayoutTrainFig3.addWidget(self.toolbar3)
        self.verticalLayoutTrainFig3.addWidget(self.canvas3)
        self.verticalLayoutTrainFig3.setAlignment(Qt.AlignCenter ) 

        self.toolbar4 = NavigationToolbar(self.canvas4,self)
        self.verticalLayoutTrainFig4.addWidget(self.toolbar4)
        self.verticalLayoutTrainFig4.addWidget(self.canvas4)
        self.verticalLayoutTrainFig4.setAlignment(Qt.AlignCenter ) 

    def getaxes(self,index):
        if(index==1):
            self.canvas1.fig.axes[0].clear()
            return self.canvas1.fig.axes[0]
        elif(index==2):
            self.canvas2.fig.axes[0].clear()
            return self.canvas2.fig.axes[0]
        elif(index==3):
            self.canvas3.fig.axes[0].clear()
            return self.canvas3.fig.axes[0]
        elif(index==4):
            self.canvas4.fig.axes[0].clear()
            return self.canvas4.fig.axes[0]
        
    def show(self,index):
        if(index==1):
            self.canvas1.draw_idle()
        elif (index==2):
            self.canvas2.draw_idle()
        elif(index==3):
            self.canvas3.draw_idle()
        elif(index==4):
            self.canvas4.draw_idle()
        super().show()
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
        self.formTrainUi=formTrainUi()
        self.formValidui=formValidUi()
  

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
             


        self.tableWidgetData.setHorizontalHeader(QtWidgets.QHeaderView(QtCore.Qt.Horizontal))
        # self.tableWidgetData.setHorizontalHeader(QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)) #python>3.6

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
        self.pushButtonValid.setEnabled(False)
        self.pushButtonTrainSaveModel.setEnabled(False)
        self.pushButtonPredict.setEnabled(False)

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


    def on_radioButtonDataUpload_toggled(self):
        self.pushButtonLoadData.setEnabled(self.radioButtonDataUpload.isChecked())
        self.checkBoxWithHeader.setEnabled(self.radioButtonDataUpload.isChecked())
        # self.pushButtonLoadData.setEnabled(False)
        self.pushButtonPredict.setEnabled(False)
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
        self.pushButtonPredict.setEnabled(True)
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
        self.pushButtonPredict.setEnabled(True)
        self.labelDataFileName.setText(QFileInfo(self.PredictDataaddress).fileName())
        if(self.checkBoxWithHeader.isChecked()):
            dataset=pd.read_csv(self.PredictDataaddress)
        else:
            dataset=pd.read_csv(self.PredictDataaddress,header=None)

        dataset=dataset.reset_index()
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
        self.tableWidgetData.setVisible(False)
        self.tableWidgetData.resizeColumnsToContents()
        self.tableWidgetData.setVisible(True)  

    def  on_tableWidgetData_cellPressed(self,row,column):
        print(row,column)
        item=self.tableWidgetData.item(row,column)
        # if(item):
        #    print(item.text())

    @QtCore.pyqtSlot()
    def on_pushButtonPredict_clicked(self):
        # if self.radioButtonDataTable.isChecked():
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
                if self.radioButtonDataTable.isChecked():
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    item.setText('0')
                self.tableWidgetData.setItem(row,0,item)
                item0=self.tableWidgetData.item(row,0)

            if(item1 and item1.text()!=''):
                pass
            else:
                item = QTableWidgetItem()
                if self.radioButtonDataTable.isChecked():
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    item.setText('0')
                
                self.tableWidgetData.setItem(row,1,item)
                item1=self.tableWidgetData.item(row,1)  
            
            time.append(float(item0.text()))
            temperature.append(float(item1.text()))
        
        self.tableWidgetData.setVisible(False)
        self.tableWidgetData.resizeColumnsToContents()
        self.tableWidgetData.setVisible(True)          
        self.PredictDataset=pd.DataFrame([*zip(time,temperature)])
        model=load_model(self.PredictModeladdress, compile = False)
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

        if(len(data.columns)<11):
            msgbox=QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("Error Message")
            msgbox.setText("Column size of dataset must be >11")
            msgbox.exec()
        else:
            
            ax=self.formTrainUi.getaxes(1)
            t= np.linspace(0,150,302)
            for i in range(len(data)):
                ax.plot(t,data.iloc[i,:])
            ax.axvline(x=5,color='black',ls='--')        
            ax.set_title("loaded Data", fontsize=10)
            ax.set_xlabel('time (s)', fontsize=10)
            ax.set_ylabel('Maximum Temperature $(^OC)$"', fontsize=10)
            ax.tick_params(axis='both', which='major',labelsize=10)
            ax.grid(True)
            self.formTrainUi.show(1)
            self.pushButtonTrain.setEnabled(True) 
            self.pushButtonValid.setEnabled(True)     

    def reset_weights(self,model):
        weights = []
        initializers = []
        for layer in model.layers:
            if isinstance(layer, (keras.layers.Dense, keras.layers.Conv2D)):
                weights += [layer.kernel, layer.bias]
                layer.kernel_initializer=keras.initializers.RandomNormal(seed=None)
                layer.bias_initializer=keras.initializers.RandomNormal(seed=None)
                initializers += [layer.kernel_initializer, layer.bias_initializer]
            elif isinstance(layer, keras.layers.BatchNormalization):
                weights += [layer.gamma, layer.beta, layer.moving_mean, layer.moving_variance]
                initializers += [layer.gamma_initializer,
                            layer.beta_initializer,
                            layer.moving_mean_initializer,
                            layer.moving_variance_initializer]
        for w, init in zip(weights, initializers):
            w.assign(init(w.shape, dtype=w.dtype))


    @QtCore.pyqtSlot()
    def on_pushButtonTrain_clicked(self):
        self.TraincurrentModel=load_model(self.TrainModeladdress, compile = False)
        print(self.TraincurrentModel.summary())
        
        if(self.checkBoxTrainWithHeader.isChecked()):
            data=self.TrainDataset.iloc[1:,:]
        else:
            data=self.TrainDataset.iloc[:,:]

        data_x=data.iloc[:,0:11].values.astype('float')
        data_y=data.iloc[:,-1].values.astype('float')
        train_x_data,test_x_data,train_y_data,test_y_data=train_test_split(data_x,data_y,
                                                                           test_size=self.doubleSpinBoxTrainSplitRate.value())

        if(self.checkBoxTrainReinitWeights.isChecked()):
            self.reset_weights(self.TraincurrentModel)

        opt=optimizers.Adam(self.doubleSpinBoxTrainLearningRate.value())
        self.TraincurrentModel.compile(loss='mse',optimizer=opt,metrics=['mse'])        
        history = self.TraincurrentModel.fit(train_x_data, train_y_data, 
                                             epochs=self.spinBoxTrainEpochNum.value(), 
                                             validation_split=self.doubleSpinBoxTrainValidationSplit.value()/100.0,
                                             batch_size=self.spinBoxTrainBatchSize.value(),
                                             verbose=0,
                                            callbacks=[CustomCallback(self.progressBarTrain,self.spinBoxTrainEpochNum.value())])
        

        predict_train_y=self.TraincurrentModel.predict(train_x_data)
        predict_test_y=self.TraincurrentModel.predict(test_x_data)

        # model evaluation
        r2_train_ann = r2_score(train_y_data, predict_train_y)
        mse_train_ann = mean_squared_error(train_y_data, predict_train_y)

        r2_test_ann = r2_score(test_y_data, predict_test_y)
        mse_test_ann = mean_squared_error(test_y_data, predict_test_y)
        # The coefficients
        print('Train R2 score: ', r2_train_ann)
        print('Train MSE: ', mse_train_ann)

        print('Test R2 score: ', r2_test_ann)
        print('Test MSE: ', mse_test_ann)

        """
            show in Fig Form
        """
        ax=self.formTrainUi.getaxes(2)
        ax.plot(history.history['loss'])
        ax.plot(history.history['val_loss'])
        ax.legend(['Training Loss', 'Validation Loss'], fontsize=10)
        ax.set_title("Training Loss", fontsize=10)
        ax.set_xlabel('Epoch', fontsize=10)
        ax.set_ylabel('Loss', fontsize=10)
        ax.tick_params(axis='both', which='major',labelsize=10)
        ax.grid(True)
        self.formTrainUi.show(2)


        ax=self.formTrainUi.getaxes(3)
        ax.scatter(train_y_data, predict_train_y, color='#2B3467')
        xline=np.arange(0,1+np.ceil(np.max([train_y_data.max(),predict_train_y.max()])))
        ax.plot(xline, xline, color='#FFB562', label = 'y = x')
        ax.legend(['train','x=y'], loc='upper left', fontsize=10)
        ax.set_title('Train: predictions', fontsize=10)
        ax.set_xlabel(r'Experimental Measured $\Delta$$T^{Train}_{max} (^oC)$', fontsize=10)
        ax.set_ylabel(r'Predicted $\Delta$$T_{max} (^oC)$', fontsize=10)
        ax.text(0,xline[-1]-1.5,'$R^{2}_{train}$='+f'{r2_train_ann:.3f}', weight='bold')
        ax.tick_params(axis='both', which='major',labelsize=10)
        ax.grid(True)
        self.formTrainUi.show(3)


        ax=self.formTrainUi.getaxes(4)
        ax.scatter(test_y_data, predict_test_y, color='#2B3467')
        xline=np.arange(0,1+np.ceil(np.max([test_y_data.max(),predict_test_y.max()])))
        ax.plot(xline, xline, color='#FFB562', label = 'y = x')
        ax.legend(['test','x=y'], loc='upper left', fontsize=10)
        ax.set_title('Test: predictions', fontsize=10)
        ax.set_xlabel(r'Experimental Measured $\Delta$$T^{Train}_{max} (^oC)$', fontsize=10)
        ax.set_ylabel(r'Predicted $\Delta$$T_{max} (^oC)$', fontsize=10)
        ax.text(0,xline[-1]-1.5,'$R^{2}_{train}$='+f'{r2_test_ann:.3f}', weight='bold')
        ax.tick_params(axis='both', which='major',labelsize=10)
        ax.grid(True)
        self.formTrainUi.show(4)

        self.pushButtonTrainSaveModel.setEnabled(True)
        
    @QtCore.pyqtSlot()
    def on_pushButtonValid_clicked(self):
        self.TraincurrentModel=load_model(self.TrainModeladdress, compile = False)
        print(self.TraincurrentModel.summary())
        
        if(self.checkBoxTrainWithHeader.isChecked()):
            data=self.TrainDataset.iloc[1:,:]
        else:
            data=self.TrainDataset.iloc[:,:]

        data_x=data.iloc[:,0:11].values.astype('float')
        data_y=data.iloc[:,-1].values.astype('float')

        predict_valid_y=self.TraincurrentModel.predict(data_x)

        # model evaluation
        r2_valid_ann = r2_score(data_y, predict_valid_y)
        mse_valid_ann = mean_squared_error(data_y, predict_valid_y)
        # The coefficients
        print('Valid R2 score: ', r2_valid_ann)
        print('Valid MSE: ', mse_valid_ann)
        """
            Fill Table
        """
        self.formValidui.fillTable(data_y,predict_valid_y)
        """
            show in Fig Form
        """

        ax=self.formValidui.getaxes(1)       
        ax.scatter(data_y, predict_valid_y, color='#2B3467')
        xline=np.arange(0,1+np.ceil(np.max([data_y.max(),predict_valid_y.max()])))
        ax.plot(xline, xline, color='#FFB562', label = 'y = x')
        ax.legend(['test','x=y'], loc='upper left', fontsize=10)
        ax.set_title('Validation: predictions', fontsize=10)
        ax.set_xlabel(r'Experimental Measured $\Delta$$T^{Valid}_{max} (^oC)$', fontsize=10)
        ax.set_ylabel(r'Predicted $\Delta$$T_{max} (^oC)$', fontsize=10)
        ax.text(0,xline[-1]-2,'$R^{2}_{train}$='+f'{r2_valid_ann:.3f}', weight='bold')
        ax.tick_params(axis='both', which='major',labelsize=10)
        ax.grid(True)
        self.formValidui.show(1)


    def closeEvent(self,event):
        print("closing app")
        self.formTrainUi.close()
        self.formValidui.close()
        event.accept()

      
"""
    Star Main code
"""
app=QApplication(sys.argv)
def main():
    # df = pd.DataFrame([[1,2,3],[4,5,6]])
    # df = pd.DataFrame([*zip([1,2,3],[4,5,6])])
    # print(df)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"]="1"
    if hasattr(QtCore.Qt,'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,True)
    if hasattr(QtCore.Qt,'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,True)    
    
    form=mainApp()
    form.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
    
    form.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                        Qt.AlignCenter,
                                        form.size(),
                                        app.primaryScreen().availableGeometry()))
    

    form.show()
    app.exec()

if __name__=="__main__":
    main()