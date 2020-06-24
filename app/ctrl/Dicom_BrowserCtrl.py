import os
import nibabel as nib

import dicom2nifti
import numpy as np
from PySide2.QtCore import QProcess
from PySide2.QtWidgets import QFileDialog, QMessageBox

from app.ctrl.DatabaseCtrl import DBCtrl
from app.ctrl.SettingsCtrl import Config, Cache
from app.ctrl.DicomImageCtrl.NJ_Segmentation import NJ_Segmentation
from app.gui.Dialogs.ProgressModal import ProgressModal
from app.ctrl.Server_connection import Client_order


class Dicom_BrowserCtrl:
    __path_for_nifti = 'data/.TestData/'
    __path_to_dicoms = '/data/.images/'
    __serie_name__: str = None
    process_modal: ProgressModal
    process: QProcess

    def __init__(self):
        self.__serie_name__: str
        self.__check_nifit_path__()
        self.__nn_segmegented_images = '/data/.nn_segemented_images/'

    def __check_nifit_path__(self):
        if not os.path.isdir(self.__path_for_nifti):
            os.mkdir(self.__path_for_nifti)

        return self.__path_for_nifti

    def image_to_nn(self, series_name: str, mask, rows: int, cols: int):
        img = nib.Nifti1Image(mask, np.eye(4))
        img.to_filename('C:/Users/kkozi/workspace/LivMDS/LivMDS/res/H-DenseUNet-master_v1/livermask/0-ori.nii')
        self.__serie_name__ = series_name
        self.__rows = rows
        self.__cols = cols

        self.process_modal = ProgressModal()
        self.process = self.init_nn_process(self.process_modal)
        self.process.readyRead.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process_modal.startButton.clicked.connect(self.run_nn_proces)
        # Client_order.send_segmented(self.__serie_name__)
        self.process_modal.exec_()

    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput(), 'utf-8').rstrip('\r\n')
        self.process_modal.print_output(text)

    def stderrReady(self):
        text = str(self.process.readAllStandardError(), 'utf-8').rstrip('\r\n')
        self.process_modal.print_error_output(text)

    def dicom_to_nifti(self):
        dicom2nifti.dicom_series_to_nifti(self.__path_to_dicoms + self.__serie_name__,
                                          self.__path_for_nifti + 'volume-0')
        return self.__path_for_nifti + 'volume-0.nii'

    def init_nn_process(self, parent):
        process = QProcess(parent)
        process.started.connect(lambda: self.process_modal.startButton.setDisabled(True))
        process.finished.connect(self.finish_nn_segmentation)

        return process

    def run_nn_proces(self):
        self.process.start(Config.get('app_dir') + '/res/run_HDense.bat',
                           [Config.get('app_dir') + self.__path_to_dicoms + self.__serie_name__,
                            Config.get('app_dir') + '/res/H-DenseUNet-master_v1/data/TestData',
                            'test-volume-0',
                            Config.get('app_dir') + self.__nn_segmegented_images,
                            str(self.__rows)])

    def finish_nn_segmentation(self):
        self.process_modal.print_output('Process finished')
        file_dialog = QFileDialog()
        file_path = file_dialog.getSaveFileName(self.process.parent(), 'Save mask as nifti', 'c:/', 'Nifit (*.nii);;')
        self.rotate_nifit(Config.get('app_dir') + '/res/H-DenseUNet-master_v1/results/test-segmentation-0.nii',
                          file_path[0])

        self.process_modal.startButton.setText("Exit")
        self.process_modal.startButton.setEnabled(True)
        self.process_modal.startButton.clicked.disconnect()
        self.process_modal.startButton.clicked.connect(self.process_modal.close)

    def send_nn_to_server(self):
        self.process_modal.print_output('Transfering file to server...')
        Client_order.send_segmented(self.__serie_name__)
        self.process_modal.print_output('File transferred to server.')

    def update_db(self):
        self.process_modal.print_output('Updating database....')
        DBCtrl().update_image_process(self.__serie_name__)
        self.process_modal.print_output('Database id updated.')

    def load_nitfit_mask(self, file_path=None):
        if file_path is None:
            file_path = self.get_nifti_file()
        mask_img = nib.load(file_path)
        mask = mask_img.get_fdata()

        return mask

    def get_nifti_file(self):
        filter = "NiFti (*.nii)"
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(filter)
        if dialog.exec():
            files = dialog.selectedFiles()[0]

            return files
        return ''

    def nj_segment(self, dicom_dir: str, points):
        method = NJ_Segmentation(dicom_dir)
        img = method.make(points[0], points[1])
        method.save_image(img, 'data/.tmp.nii')

    @staticmethod
    def save_mask(parent, mask, path=None):
        if path is None:
            file_dialog = QFileDialog()
            file = file_dialog.getSaveFileName(parent, 'Save mask as nifti', 'c:/', 'Nifit (*.nii);;')
            path = file[0]
        img = nib.Nifti1Image(mask, np.eye(4))
        img.to_filename(path)

    @property
    def nifit_path(self):
        return self.__path_for_nifti

    @nifit_path.setter
    def nifit_path(self, path: str):
        self.__path_for_nifti = path

    @property
    def dicom_path(self):
        return self.__path_to_dicoms

    @dicom_path.setter
    def dicom_path(self, path: str):
        self.__path_to_dicoms = path

    def rotate_nifit(self, file_in, path_out):
        img = nib.load(file_in)
        img = np.rot90(img.get_fdata())
        new_img = np.zeros([img.shape[0], img.shape[1], img.shape[2]], np.int)

        for slice_num in range(0, img.shape[2]):
            new_img[:, :, slice_num] = img[:, :, slice_num]
        img = nib.Nifti1Image(new_img, np.eye(4))
        img.to_filename(path_out)


if __name__ == '__main__':
    ctrl = Dicom_BrowserCtrl()
    ctrl.rotate_nifit(
        'C:/Users/kkozi/workspace/LivMDS/LivMDS/res/H-DenseUNet-master_v1/results/test-segmentation-0.nii',
        'C:/Users/kkozi/workspace/LivMDS/LivMDS/eee.nii')
