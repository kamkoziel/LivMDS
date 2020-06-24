import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QProgressDialog, QMessageBox

from app.ctrl.PACS_ServerCtrl import PACS_ServerCtrl
from app.ctrl.PACS_OrthancCtrl import PACS_OrthancServerCtrl


class PACS_MainCtrl():
    __path_for_dicoms = 'data/.images'
    __pacs: PACS_ServerCtrl

    def __init__(self, **kwargs):
        self.__check_dicom_path()
        self.pacs_server = kwargs.get('serwer', PACS_OrthancServerCtrl())

    @staticmethod
    def get_serie(instances):
        ctrl = PACS_MainCtrl()
        path = ctrl.dicom_path + '/{0}'.format(instances[0]['ParentSeries'])

        try:
            if not os.path.isdir(path):
                os.mkdir(path)
        finally:
            progress_modal = QProgressDialog('PACS loading files', 'Cancel', 1, len(instances))
            progress_modal.setWindowModality(Qt.WindowModal)

        instance_num = 1
        for instance in instances:
            ctrl.load_dicom(path, instance)
            progress_modal.setValue(instance_num)
            instance_num = instance_num + 1

        return path

    def update_stage(self):
        pass

    def load_dicom(self, path, instance):
        filepath = path + '/DCM{0}'.format(instance['IndexInSeries'])
        if not os.path.exists(filepath + '.dcm'):
            self.pacs_server.move(instance['ID'], filepath)

    def __check_dicom_path(self):
        try:
            if not os.path.isdir(self.dicom_path):
                os.mkdir(self.dicom_path)
        finally:
            return self.dicom_path

    @property
    def dicom_path(self): return self.__path_for_dicoms

    @property
    def pacs_server(self): return self.__pacs

    @pacs_server.setter
    def pacs_server(self, serwer_ctrl: PACS_ServerCtrl):
        self.__pacs = serwer_ctrl
