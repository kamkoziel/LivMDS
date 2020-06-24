from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout

from app.ctrl.Utils import get_style
from app.models.PACS_Stage import PACS_Stage


class PACS_StagesBar(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.setMaximumHeight(35)

        self.initUI()

    def initUI(self):
        self.patientBtn = self.__initButton('Patient >')
        self.studyBtn = self.__initButton('Study >')
        self.seriesBtn = self.__initButton('Serie ')

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.patientBtn)
        layout.addWidget(self.studyBtn)
        layout.addWidget(self.seriesBtn)

    def __initButton(self, text :str):
        button = QPushButton(text)
        button.setStyleSheet(get_style('res/styles/stage_btn_style.css'))
        return button

    def set_stage(self, stage: PACS_Stage):
        if stage is PACS_Stage.PATIENT:
            self.patientBtn.setDisabled(False)
            self.studyBtn.setDisabled(True)
            self.seriesBtn.setDisabled(True)

        elif stage is PACS_Stage.STUDY:
            self.patientBtn.setDisabled(False)
            self.studyBtn.setDisabled(False)
            self.seriesBtn.setDisabled(True)

        elif stage is PACS_Stage.SERIES:
            self.patientBtn.setDisabled(False)
            self.studyBtn.setDisabled(False)
            self.seriesBtn.setDisabled(False)
        elif stage is PACS_Stage.INSTANCE:
            pass
