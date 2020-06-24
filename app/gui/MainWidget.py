from PySide2.QtCore import QMargins
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QDockWidget, QMessageBox

from app.gui.MenuLeftPane import MenuLeftPane
from app.gui.Dicom_Browser import Dicom_Browser
from app.gui.PACS_Widget import PACS_MainWidget
from app.gui.LiverSupportWidget import LiverSupportWidget
from app.ctrl.PACS_ServerCtrl import PACS_ServerCtrl
from app.ctrl.PACS_OrthancCtrl import PACS_OrthancServerCtrl


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.username = parent.user
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.leftPanelWidth = 250
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.initUI()

    def initUI(self):
        self.pacs_ctrl: PACS_ServerCtrl = PACS_OrthancServerCtrl()
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.pacs_widget = PACS_MainWidget()
        self.dicom_widget = Dicom_Browser()
        # self.liver_support_widget = LiverSupportWidget()
        self.button_bar = MenuLeftPane()

        topLayout = QVBoxLayout()
        topLayout.setAlignment(Qt.AlignTop)
        topLayout.addWidget(self.button_bar)

        self.mainWidget = QDockWidget()
        self.mainWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.mainWidget.setTitleBarWidget(QWidget())
        self.mainWidget.setWidget(self.dicom_widget)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.mainWidget)

        self.button_bar.pacs_btn.clicked.connect(self.show_PACSWidget)
        self.button_bar.dcm_btn.clicked.connect(self.show_DICOMBrowser)
        # self.button_bar.liv_support_btn.clicked.connect(self.show_liverSupport)
        self.pacs_widget.dcm_to_browser.connect(self.send_file_to_browser)

        self.show_PACSWidget()

    def show_PACSWidget(self):
        connect = self.pacs_ctrl.isConnect()
        if connect:
            self.mainWidget.setWidget(self.pacs_widget)
            self.button_bar.pacs_btn.setDisabled(1)
            self.button_bar.dcm_btn.setDisabled(0)
            # self.button_bar.liv_support_btn.setDisabled(0)
        else:
            QMessageBox.warning(
                self, 'Connect Error',
                '''Application is not able to connect with PACS Server                      
                    Check Klient and Archive data ''', QMessageBox.Ok)

    def show_DICOMBrowser(self):
        self.mainWidget.setWidget(self.dicom_widget)
        self.button_bar.dcm_btn.setDisabled(1)
        self.button_bar.pacs_btn.setDisabled(0)
        # self.button_bar.liv_support_btn.setDisabled(0)

    # def show_liverSupport(self):
    #     self.mainWidget.setWidget(self.liver_support_widget)
    #     self.button_bar.pacs_btn.setDisabled(0)
    #     self.button_bar.dcm_btn.setDisabled(0)
    #     self.button_bar.liv_support_btn.setDisabled(1)

    def send_file_to_browser(self, path):
        self.mainWidget.setWidget(self.dicom_widget)
        self.dicom_widget.load_series(path)
        self.dicom_widget.series_id = self.pacs_widget.stage_chain['series']
        self.button_bar.dcm_btn.setDisabled(1)
        self.button_bar.pacs_btn.setDisabled(0)
