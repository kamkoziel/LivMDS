Liver Medical Diagnosis Support
=========

Tested: 

+PACS server - Orthanc

+Operating system - Win10

+Python version: 3.7 (don't try on Python 2.x)

## Required programs
+ Python 3.7 (include pip and virtualenv) [link](https://www.python.org/downloads/)
+ Anaconda (conda in system PATH) [link](https://www.anaconda.com)
+ Configured PACS Orthanc Server [link](https://www.orthanc-server.com/download-windows.php)
+ Postgresql Server with created empty database  [link](https://www.postgresql.org/download/)

## Prepare virtual environment

First step to run application is create new python virtual environment run before_start.bat
or type in command line:

``` python
python -m venv livmds_env
.\livmds\Scripts\activate.bat    
pip install -r requirements.txt  
```
## Prepare anaconda env
Get H-DenseUNet from [here](https://1drv.ms/u/s!AnCn6ekzG7Q2hbYYj6zqZVxqwrFuMA?e=IEy2Ew)
Find anaconda envs directory and move there H-DenseUNet from zip

## Get model file for nn segment feature
Get hd5 file from [here](https://drive.google.com/file/d/1Qo4TFR4hf5wVPJSkMqGMEf4O4GjRHRyU/view)
Put it to LivMDS\res\HDense-UNet-master_v1\model


## Running app
To run app you should run you command prompt from app directory and then type or run LivMDS_start.bat:
``` bash
python LiverMDS.py.py
```
