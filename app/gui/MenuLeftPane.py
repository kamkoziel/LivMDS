from PySide2.QtCore import Qt, QMargins
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QGroupBox

from app.ctrl.Utils import get_style


class MenuLeftPane(QWidget):
    style_path = 'res/styles/menu_pane_style.css'

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet(get_style(self.style_path))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.initUI()

    def initUI(self):
        self.group = QGroupBox()
        self.pacs_btn = self.__initButton('PACS Module')
        self.dcm_btn = self.__initButton('Dicom Browser')
        # self.liv_support_btn = self.__initButton('Diagnosis Support')

        boxlayout = QVBoxLayout(self)
        boxlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        boxlayout.setContentsMargins(QMargins(0, 0, 0, 0))
        boxlayout.setSpacing(0)
        boxlayout.addWidget(self.pacs_btn)
        boxlayout.addWidget(self.dcm_btn)
        # boxlayout.addWidget(self.liv_support_btn)

        self.group.setLayout(boxlayout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        layout.addWidget(self.group)

    def __initButton(self, text: str):
        button = QPushButton(text)
        button.setContentsMargins(QMargins(0, 0, 0, 0))

        return button
