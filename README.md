# GUI for AI Thermometry prediction
This is the repository containing GUI for predication of temretaure rise around tip of active implant (like DBS) during RF pulse with AI models , is developing in RadLab.

Firts 5 second(with 0.5 s resolution =11 points) of temperature profile upload and the model predict temperature of plateau (~150s).

Packages Installation:

    conda create -n radlab
    activate  radlab
    conda install tensorflow keras
    conda install pyqt
    pip install pyqt5-tools
    conda install pandas
    conda intsall matplotlib

converting Ui to Py files:

    pyuic5 Ui\mainUi.ui -o uiMain.py

Convert py files to one main executable file:

    pyinstaller   --onefile   main.py -n main.exe

Note:it took ~25s to load GUI
## How Use
1.in Predict Tab select Model from combobox  or load h5 model ("..." pushbutton).

>Note: Model combobox finds your models in Models folder in the root of .exe file

2.Select type ofData:

>2.1 "Upload Data": select a cvs file (time,temperature) for 11 initial points.If data have header select "With header" checkbox.Then press "Load" button to show in Table

or

>2.2 "Table": write time and Temperature in Table

3.Press "predict" Button, wait ~2 second
