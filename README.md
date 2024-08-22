# GUI for AI Thermometry prediction
This is the repository containing GUI for predication of temretaure rise around tip of active implant (like DBS) during RF pulse with AI models , is developing in RadLab.

Firts 5 second(with 0.5 s resolution =11 points) of temperature profile upload and the model predict temperature of plateau (~150s).

Packages Installation:

    conda create -n radlab
    activate  radlab
    conda install tensorflow keras=2.10.0
    conda install pyqt
    pip install pyqt5-tools
    conda install pandas=2.2.2
    conda intsall matplotlib
    conda install anaconda::scikit-learn=1.5.1
    pip install pyinstaller==6.6

converting Ui to Py files:

    pyuic5 Ui\mainUi.ui -o uiMain.py

Convert py files to one main executable file:

     pyinstaller   --onefile  main.py -n main.exe --distpath=.

Note:it took ~25s to load GUI
## How Use
### Predict Tab
1. in Predict Tab select Model from combobox  or load h5 model ("..." pushbutton).

>Note: Model combobox finds your models in Models folder in the root of .exe file

2. Select type of Data:

    2.1 "Upload Data": select a cvs file (time,temperature) for 11 initial points.If data have header select "With header" checkbox.Then press "Load" button to show in Table

    2.2 "Table": write time and Temperature in Table

3. Press "predict" Button, wait ~2 second and the results will be shown in "Predict Temperature"

### Train Tab 

1. in Train Tab select Model from combobox  or load h5 model ("..." pushbutton).

2. set Train Parmeters 

3.  in Dataset box  "Select Data File"
> Note: File in CSV format and each row contain of samples at least 11 column (0:0.5:5s and the last column maximum temperature ).if Data have header tick "with header"
4. Press "Load" to load adta and the figure will be shown
5. Press "Train"   to train selected model.if you need reset weights select "Reset weights"
6. the Loss values will be shown
7. if you need "save" the model
