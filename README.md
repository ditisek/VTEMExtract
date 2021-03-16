# VTEMExtract

Extraction tool for Geotech VTEM system

Windows executable can be found in the dist folder. Maker sure to have the **Geotech.bmp** and **kst.dat** file in the same folder when running the application to ensure proper operation.

Be carefull when selecting the **Remove D Files** option as all the files will be cleaned out of your workng directory.

To run the python code the following libraries are required:
* **wxPython** - _install using:_ _**pip install wxPython**_
* **geotech** - _can be downloaded and installed from github or use a direct pull with:_ _**pip install git+https://github.com/ditisek/geotech.git**_