Liver Medical Diagnosis Support
=========

Tested: 

+PACS server - dcmqrscp 

+Operating system - Win10

+Python version: 3.7 (don't try on Python 2.x)

## Required programs
+ Python 3.7 (include pip and virtualenv)
+ Anaconda (conda in system PATH)
+ Configured PACS Orthanc Server
+ Postgresql Server with created empty database 

## Prepare virtual environment

First step to run application is create new python virtual environment

``` python
python3 -m venv venv
```
Next you have to active your environment
``` bash
 venv\Scripts\activate.bat
``` 
## Install requirements packages
``` bash
(venv) (...)> pip install (path_to_PACSClient)\requirements.txt
```
## Add gdcm dll to you Python directory

Copy files from res\dlls to C:\Users\(username)\AppData\Local\Programs\Python\Python37\DLLs

## Running app
To run app you should run you command prompt from StepToBum directory and then type:
``` bash
(venv) (path_to_PACSClient) > python PACSClient.py
```
