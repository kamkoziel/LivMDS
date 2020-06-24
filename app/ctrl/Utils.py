# TODO
#  first start wizard
#  no orthanc exeption catch
import os

from app.ctrl.SettingsCtrl import Config


def start_app():
    generate_nn_bat()


def get_style(path: str):
    """ Return CSS file content in string format"""

    css_file = open(path, 'r')
    style = css_file.read()

    return style

def get_app_dir() -> str :
    return os.getcwd()

def generate_nn_bat():
    path = Config.get('app_dir') + '/res/run_HDense.bat'
    content = '''
@ECHO OFF
Rem args :  %1 - input dicom dir path
Rem         %2 - output nifti path
Rem         %3 - output nifti file name
Rem         %4 - result save path
Rem         %5 - input size

ECHO '##################'
ECHO 'Script is starting with params: '
ECHO 'Input input path: ' %1
ECHO 'Output nifti dir path: ' %2
ECHO 'Output nifti file name: ' %3
ECHO 'Result save path: ' %4
ECHO 'Input size: ' %5
ECHO '#########################'

del "{0}" /s /f /q

ECHO 'Conda  activate ...'
call conda.bat activate H-DenseUNet
ECHO 'Conda READY'
ECHO 'Converting dicom to nifti ...'
dcm2niix -f volume-0 -o %2 %1
del "{1}" /s /f /q
ECHO 'Converting dicom to nifti - DONE'
ECHO 'Preprocessing start ...'

cd "{2}"
ECHO 'Starting preprocesing...'
python preprocessing.py
ECHO 'Preprocessing - DONE'
ECHO 'Starting H-DenseUNet segmentation....'
python test.py -input_size %5 '''.format(Config.get('app_dir') + '\\res\\H-DenseUNet-master_v1\\data\\TestData\\*.*',
                                         Config.get('app_dir') + '\\res\\H-DenseUNet-master_v1\\data\\TestData\\volume-0.json',
                                         Config.get('app_dir') + '\\res\\H-DenseUNet-master_v1')

    f = open(path, "w")
    f.write(content)
    f.close()

