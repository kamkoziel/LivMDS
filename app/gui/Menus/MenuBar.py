from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMenuBar, QAction, QApplication, QFileDialog

from app.gui.Dialogs.SettingsDialog import SettingDialog
from app.gui.MainWidget import MainWidget


class MenuBar(QMenuBar):
    def __init__(self, main_widget: MainWidget):
        QMenuBar.__init__(self)
        self.main_widget = main_widget

        fileMenu = self.addMenu('&File')
        fileMenu.addAction(self.open_dcm_action())
        fileMenu.addAction(self.settings_action())
        fileMenu.addSeparator()
        fileMenu.addAction(self.exit())

    def exit(self):
        act = QAction(QIcon('exit.png'), '&Exit', self)
        act.setShortcut('Ctrl+Q')
        act.setStatusTip('Exit application')
        act.triggered.connect(QApplication.instance().quit)

        return act

    def open_dcm_action(self):
        act = QAction(QIcon('exit.png'), 'Open dicom', self)
        act.setStatusTip('Open dicom images')
        act.triggered.connect(self.open_dcm)
        return act

    def settings_action(self):
        act = QAction(QIcon('exit.png'), 'Settings', self)
        act.setStatusTip('Set connecting and other properties')
        act.triggered.connect(self.settings)
        return act

    def open_dcm(self):
        filter = "DICOM (*.dcm)"
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(filter)
        if dialog.exec():
            files = dialog.selectedFiles()
            try:
                self.main_widget.send_file_to_browser(files)
            finally:
                return

    def settings(self):
        SettingDialog.show_dialog(self)

