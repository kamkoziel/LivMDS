from PySide2.QtGui import QColor
from PySide2.QtWidgets import QDialog, QTextEdit, QPushButton, QLabel
from PySide2.QtWidgets import QVBoxLayout

from app.ctrl.PACS_ServerCtrl import PACS_ServerCtrl
from app.ctrl.PACS_OrthancCtrl import PACS_OrthancServerCtrl


class ProgressModal(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('PACS loading files')
        self.pacs_ctrl: PACS_ServerCtrl = PACS_OrthancServerCtrl()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Are you sure you want to start the segmentation process? This can take a long time')
        self.proges_output = QTextEdit()
        self.proges_output.isReadOnly()
        self.startButton = QPushButton('Start')

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.proges_output)
        layout.addWidget(self.startButton)
        self.setLayout(layout)

    def print_output(self, text):
        self.proges_output.setTextColor(QColor(0, 0, 0))
        self.proges_output.append(text)

    def print_error_output(self, text):
        self.proges_output.setTextColor(QColor(255, 0, 0))
        self.proges_output.append(text)




