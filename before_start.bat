@ECHO OFF

ECHO PREPARING virtualenv env...
python -m virtualenv livmds_env
ECHO Activate livmds-env...
.\livmds_env\Scripts\activate.bat
ECHO Installing packages...
pip install -r requirements.txt
ECHO livmds-env ready!

