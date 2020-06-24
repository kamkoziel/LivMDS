from PySide2.QtCore import Qt

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QMessageBox, QCheckBox
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout

from app.ctrl.SettingsCtrl import Config
from app.ctrl.Utils import get_style, get_app_dir


class SettingDialog(QDialog):
    style_path = 'res/styles/register_dialog_style.css'

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)

        self.setWindowTitle('Settings')
        self.setStyleSheet(get_style(self.style_path))
        self.initUI()
        self.fill_fields()

    def initUI(self):
        orthanc_pacs_adres = QLabel('''Orthanc adres 
(must start with http:// or https://):''')
        orthanc_pacs_login = QLabel('Orthanc login:')
        orthanc_pacs_password = QLabel('Orthanc password:')

        self.pacs_adres = QLineEdit()
        self.pacs_login = QLineEdit()
        self.pacs_password = QLineEdit()
        self.pacs_password.setEchoMode(QLineEdit.Password)

        self.db_host = QLineEdit()
        self.db_name = QLineEdit()
        self.db_user = QLineEdit()
        self.db_password = QLineEdit()
        self.db_password.setEchoMode(QLineEdit.Password)

        self.dont_show_settings_startup = QCheckBox()

        leftLayoutColumn = QVBoxLayout()
        leftLayoutColumn.addWidget(orthanc_pacs_adres)
        leftLayoutColumn.addWidget(orthanc_pacs_login)
        leftLayoutColumn.addWidget(orthanc_pacs_password)
        leftLayoutColumn.addWidget(QLabel('--------------------------'))
        leftLayoutColumn.addWidget(QLabel('Postgres db host'))
        leftLayoutColumn.addWidget(QLabel('Postgres db name'))
        leftLayoutColumn.addWidget(QLabel('Postgres db user'))
        leftLayoutColumn.addWidget(QLabel('Postgres db password'))
        leftLayoutColumn.addWidget(QLabel('Don\'t show this window at start '))

        rightLayoutColumn = QVBoxLayout()
        rightLayoutColumn.addWidget(self.pacs_adres)
        rightLayoutColumn.addWidget(self.pacs_login)
        rightLayoutColumn.addWidget(self.pacs_password)
        rightLayoutColumn.addWidget(QLabel('  '))
        rightLayoutColumn.addWidget(self.db_host)
        rightLayoutColumn.addWidget(self.db_name)
        rightLayoutColumn.addWidget(self.db_user)
        rightLayoutColumn.addWidget(self.db_password)
        rightLayoutColumn.addWidget(self.dont_show_settings_startup)

        topLayout = QHBoxLayout()
        topLayout.addLayout(leftLayoutColumn)
        topLayout.addLayout(rightLayoutColumn)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(topLayout)
        layout.addWidget(self.buttons)

    @staticmethod
    def show_dialog(parent=None):
        dialog = SettingDialog()
        ok = dialog.exec_()
        return ok

    def accept(self):
        self.update_config()

    def update_config(self):
        if self.pacs_adres.text().strip() or self.pacs_login.text().strip() or self.pacs_password.text().strip():
            Config.update('app_dir', get_app_dir())
            Config.update('pacs_adres', self.pacs_adres.text())
            Config.update('pacs_login', self.pacs_login.text())
            Config.update('pacs_password', self.pacs_password.text())
            Config.update('db_host', self.db_host.text())
            Config.update('db_name', self.db_name.text())
            Config.update('db_user', self.db_user.text())
            Config.update('db_password', self.db_password.text())
            Config.update('dont_show_settings_startup', self.dont_show_settings_startup.isChecked())

            super().accept()
        else:
            QMessageBox.warning(self, 'Error', 'All field are required')

    def fill_fields(self):
        self.pacs_adres.setText(Config.get('pacs_adres'))
        self.pacs_login.setText(Config.get('pacs_login'))
        self.pacs_password.setText(Config.get('pacs_password'))
        self.db_host.setText(Config.get('db_host'))
        self.db_name.setText(Config.get('db_name'))
        self.db_user.setText(Config.get('db_user'))
        self.db_password.setText(Config.get('db_password'))
        if Config.get('dont_show_settings_startup'):
            self.dont_show_settings_startup.setChecked(True)
