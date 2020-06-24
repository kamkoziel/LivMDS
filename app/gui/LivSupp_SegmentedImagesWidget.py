from PySide2.QtWidgets import QWidget, QTableView, QVBoxLayout

from app.ctrl.LiverSupportCtrl import LiverSupportCtrl
from app.models.LiverSupport_SegmentedImagesModel import LiverSupport_SegmentedImagesModel


class LivSupp_SegmentedImagesWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.view = QTableView()
        self.model = LiverSupport_SegmentedImagesModel(LiverSupportCtrl().get_images())
        self.view.setModel(self.model)
        self.view.setColumnHidden(2, True)
        self.view.setColumnHidden(3, True)
        self.view.setColumnHidden(4, True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

