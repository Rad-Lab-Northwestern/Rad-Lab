# GUI for AI Thermometry prediction
This is the repository containing GUI for predication of temretaure rise around tip of active implant (like DBS) during RF pulse with AI models , is developing in RadLab.

Firts 5 second(with 0.5 s resolution =11 points) of temperature profiel upload and the model predict temperature after 150s.

Packages Installation:

    conda create -n <env name> python=3.6
    pip install pyqt5-tools
    conda intsall tensorflow
    conda install jupyter
    conda install scikit-learn
    conda install seaborn
    pip install pyinstaller

converting Ui to Py files:

    pyuic5 Ui\mainUi.ui -o uiMain.py

Convert py files to one main executable file:

    pyinstaller --noconsole  --onefile --windowed main.py -n main.exe