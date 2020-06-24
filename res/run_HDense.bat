
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

del "C:\Users\kkozi\workspace\LivMDS\LivMDS\res\H-DenseUNet-master_v1\data\TestData\*.*" /s /f /q

ECHO 'Conda  activate ...'
call conda.bat activate H-DenseUNet
ECHO 'Conda READY'
ECHO 'Converting dicom to nifti ...'
dcm2niix -f volume-0 -o %2 %1
del "C:\Users\kkozi\workspace\LivMDS\LivMDS\res\H-DenseUNet-master_v1\data\TestData\volume-0.json" /s /f /q
ECHO 'Converting dicom to nifti - DONE'
ECHO 'Preprocessing start ...'

cd "C:\Users\kkozi\workspace\LivMDS\LivMDS\res\H-DenseUNet-master_v1"
ECHO 'Starting preprocesing...'
python preprocessing.py
ECHO 'Preprocessing - DONE'
ECHO 'Starting H-DenseUNet segmentation....'
python test.py -input_size %5 