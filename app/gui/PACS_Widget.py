from PySide2.QtWidgets import QWidget, QFileSystemModel, QTreeView, QMessageBox, QVBoxLayout, QProgressDialog
from PySide2.QtWidgets import QHBoxLayout, QSplitter
from PySide2.QtCore import Signal, QAbstractTableModel, Qt
from app.ctrl.PACS_ServerCtrl import PACS_ServerCtrl
from app.ctrl.PACS_MainCtrl import PACS_MainCtrl
from app.ctrl.PACS_OrthancCtrl import PACS_OrthancServerCtrl
from app.gui.Dialogs.ProgressModal import ProgressModal
from app.gui.PACS_ItemView import PACSItemView
from app.gui.PACS_StagesBar import PACS_StagesBar
from app.models.PACS_PatientsTabModel import PACS_PatientsTabModel
from app.models.PACS_SeriesTabModel import PACS_SeriesTabModel
from app.models.PACS_Stage import PACS_Stage
import os
import glob


class PACS_MainWidget(QWidget):
    dcm_to_browser = Signal(object)
    pacs_model: QAbstractTableModel

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 650
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.stage = PACS_Stage.PATIENT
        self.stage_chain = {'patient': None,
                            'study': None,
                            'series': None}

        self.initUI()

    def initUI(self):
        self.stages_bar = PACS_StagesBar()
        self.stages_bar.set_stage(self.stage)

        self.files_system_model = self.__initFilesSystemModel__()
        self.files_system_view = self.__initFileTreeView__(self.files_system_model)

        self.pacs_view = PACSItemView()
        self.setPatientsModel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.stages_bar)
        layout.addWidget(self.pacs_view)

        self.files_system_view.doubleClicked.connect(self.storeItem)
        self.pacs_view.doubleClicked.connect(self.next_stage)
        self.stages_bar.patientBtn.clicked.connect(self.back_to_patient)
        self.stages_bar.studyBtn.clicked.connect(self.back_to_study)
        self.stages_bar.seriesBtn.clicked.connect(self.bact_to_series)

    def __initFileTreeView__(self, model):
        treeView = QTreeView()
        treeView.setIndentation(20)
        treeView.setSortingEnabled(True)
        treeView.setMinimumWidth(100)
        treeView.setModel(model)
        treeView.setRootIndex(model.index(r'C:'))

        for i in range(1, 5):
            treeView.hideColumn(i)

        return treeView

    def __initFilesSystemModel__(self):
        model = QFileSystemModel()
        model.setRootPath(r'C:')
        model.setReadOnly(True)

        return model

    def storeItem(self, index):
        pass

    def next_stage(self):
        if self.stage is PACS_Stage.PATIENT:
            self.stage = PACS_Stage.STUDY
            self.update_stage()
        elif self.stage is PACS_Stage.STUDY:
            self.stage = PACS_Stage.SERIES
            self.update_stage()
        elif self.stage is PACS_Stage.SERIES:
            self.stage = PACS_Stage.INSTANCE
            self.update_stage()
        elif self.stage is PACS_Stage.INSTANCE:
            pass

    def update_stage(self):
        if self.stage is PACS_Stage.PATIENT:
            self.setPatientsModel()
            self.stages_bar.set_stage(self.stage)

        elif self.stage is PACS_Stage.STUDY:
            self.setStudiesModel()
            self.stages_bar.set_stage(self.stage)

        elif self.stage is PACS_Stage.SERIES:
            self.setSeriesModel()
            self.stages_bar.set_stage(self.stage)

        elif self.stage is PACS_Stage.INSTANCE:
            self.openSeriesImages()
            self.stages_bar.set_stage(self.stage)

    def set_stage(self, stage: PACS_Stage):
        self.stage = stage
        self.update_stage()

    def setPatientsModel(self):
        ctrl = PACS_OrthancServerCtrl()
        self.pacs_model = PACS_PatientsTabModel([''])
        if ctrl.isConnect():
            try:
                patients = ctrl.find()
                self.pacs_model.update(patients)
            except Exception as e:
                QMessageBox.warning(self, 'Problem', 'Error on loading patients list: {0}'.format(e))
            finally:
                self.pacs_view.setModel(self.pacs_model)

    def setStudiesModel(self):
        ctrl = PACS_OrthancServerCtrl()
        if self.stage_chain['patient'] is None:
            index = self.pacs_view.selectedIndexes()
            self.stage_chain['patient'] = self.pacs_view.model().itemData(index[0])[0]

        studies = ctrl.find_study(self.stage_chain['patient'])
        self.pacs_model = PACS_SeriesTabModel(studies)
        self.pacs_view.setModel(self.pacs_model)

    def setSeriesModel(self):
        ctrl = PACS_OrthancServerCtrl()
        try:
            index = self.pacs_view.selectedIndexes()
            self.stage_chain['study'] = self.pacs_view.model().itemData(index[0])[0]
        finally:
            series = ctrl.find_series(self.stage_chain['study'])
            self.pacs_model = PACS_SeriesTabModel(series)
            self.pacs_view.setModel(self.pacs_model)

    def openSeriesImages(self):
        ctrl = PACS_OrthancServerCtrl()
        index = self.pacs_view.selectedIndexes()
        self.stage_chain['series'] = self.pacs_view.model().itemData(index[0])[0]
        instances = ctrl.find_instance(self.stage_chain['series'])
        path = PACS_MainCtrl.get_serie(instances)

        self.pacs_view.clearSelection()
        self.dcm_to_browser.emit(path + '/')

    def back_to_patient(self):
        self.stage_chain['patient'] = None
        self.stage_chain['study'] = None
        self.stage_chain['series'] = None
        self.set_stage(PACS_Stage.PATIENT)

    def back_to_study(self):
        self.stage_chain['study'] = None
        self.stage_chain['series'] = None
        self.set_stage(PACS_Stage.STUDY)

    def bact_to_series(self):
        self.stage_chain['series'] = None
        self.set_stage(PACS_Stage.SERIES)
