from PySide2.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGroupBox, QSlider, QTabWidget, QPushButton, QDockWidget
from PySide2.QtWidgets import QHBoxLayout, QSplitter

import os

from app.gui.LivSupp_SegmentedImagesWidget import LivSupp_SegmentedImagesWidget


class LiverSupportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.segmented_images = LivSupp_SegmentedImagesWidget()
        self.dockWidget = QDockWidget()
        self.dockWidget.setTitleBarWidget(QWidget())
        self.dockWidget.setWidget(self.segmented_images)

        layout = QVBoxLayout(self)
        layout.addWidget(self.dockWidget)



