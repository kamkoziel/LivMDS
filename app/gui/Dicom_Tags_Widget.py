from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableView
from app.models.Dicom_TagsModel import Dicom_TagsModel


class Dicom_Tags_Widget(QWidget):
    __tab_name__ = 'Dicom Tags'

    def __init__(self, data):
        super().__init__()

        self.init_ui(data)

    def init_ui(self, data):
        self.model = Dicom_TagsModel(data)
        self.view = QTableView()
        self.view.setModel(self.model)

        layout = QHBoxLayout(self)
        layout.addWidget(self.view)

    def __get_tab_name(self):
        return self.__tab_name__

    tab_name = property(__get_tab_name)






