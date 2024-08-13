import sys
import  os
from time import sleeep

"""
    Qt import
"""

"""
    AI import
"""
# import tesnsorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras import activations
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import metrics
from tensorflow.keras import backend as K
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,KFold


"""
    MainApp Class
"""
class mainApp():
    def __init__(self,parent=None):
        super(mainApp,self).__init__(parent)
        
def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"]="1"
    app=QApplication(sys.argv)
    form=mainApp()
    form.setWindowFlags(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
    form.show()
    app.exec()
if __name__=="__main__":
    main()