import json

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from PySide2.QtWidgets import QDialog, QPushButton, QDialogButtonBox, QMessageBox, QLabel, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from app.ctrl.DatabaseCtrl import DBCtrl
from app.ctrl.Utils import get_style
from app.gui.Dialogs import SettingsDialog
from app.gui.Dialogs.RegisterDialog import RegisterDialog
from app.gui.Dialogs.SettingsDialog import SettingDialog


class LoginDialog(QDialog):
    style_path = 'res/styles/login_dialog_style.css'

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)

        self.setWindowTitle('Login')
        self.setStyleSheet(get_style(self.style_path))
        self.initUI()

    def initUI(self):
        usernameLabel = QLabel('Username:')
        passwordLabel = QLabel('Password:')
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.add_user_btn = QPushButton("Sign up")
        self.add_user_btn.clicked.connect(self.open_registration_modal)

        leftLayoutColumn = QVBoxLayout()
        leftLayoutColumn.addWidget(usernameLabel)
        leftLayoutColumn.addWidget(passwordLabel)

        rightLayoutColumn = QVBoxLayout()
        rightLayoutColumn.addWidget(self.username)
        rightLayoutColumn.addWidget(self.password)

        topLayout = QHBoxLayout()
        topLayout.addLayout(leftLayoutColumn)
        topLayout.addLayout(rightLayoutColumn)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(topLayout)
        layout.addWidget(self.add_user_btn)
        layout.addWidget(self.buttons)

    def showWidget(self, parent=None):
        dialog = LoginDialog(parent)
        ok = dialog.exec_()
        return ok

    def accept(self):
        user_auth = False
        try:
            user_auth, user_data = DBCtrl().is_user(name=self.username.text(), password=self.password.text())
        except Exception:
            QMessageBox.warning(self, 'Error', 'No connection with db')
            SettingDialog.show_dialog(self)

        if user_auth:
            session = DBCtrl().open_session(user_data['id'])
            self.make_cache(user_data, session['id'])
            super().accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong login or password')

    def username_auth(self):
        return self.username.text()

    def open_registration_modal(self):
        register = RegisterDialog()
        if register.exec_() == QtWidgets.QDialog.Accepted:
            QMessageBox.information(self, 'Success', 'Registration success')

    def make_cache(self, user_data, session_id=1):
        cache_path = 'res/.cache.json'

        # save cache to *.json file
        with open(cache_path, 'w') as cache_file:
            json.dump({
                'user_id': user_data['id'],
                'user_name': user_data['name'],
                'session_id': int(session_id)}, cache_file, indent=4)
