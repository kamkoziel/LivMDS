from PySide2.QtCore import Qt

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QLabel, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from sqlalchemy.exc import IntegrityError

from app.ctrl.DatabaseCtrl import DBCtrl
from app.ctrl.Utils import get_style


class RegisterDialog(QDialog):
    style_path = 'res/styles/register_dialog_style.css'

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)

        self.setWindowTitle('Register here')
        self.setStyleSheet(get_style(self.style_path))
        self.initUI()

    def initUI(self):
        usernameLabel = QLabel('Username:')
        passwordLabel = QLabel('Password:')
        repasswordLabel = QLabel('Repeat password:')
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.re_password = QLineEdit()
        self.re_password.setEchoMode(QLineEdit.Password)

        leftLayoutColumn = QVBoxLayout()
        leftLayoutColumn.addWidget(usernameLabel)
        leftLayoutColumn.addWidget(passwordLabel)
        leftLayoutColumn.addWidget(repasswordLabel)

        rightLayoutColumn = QVBoxLayout()
        rightLayoutColumn.addWidget(self.username)
        rightLayoutColumn.addWidget(self.password)
        rightLayoutColumn.addWidget(self.re_password)

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

    def showWidget(self, parent=None):
        dialog = RegisterDialog(parent)
        ok = dialog.exec_()
        return ok

    def accept(self):
        if self.password.text() != self.re_password.text():
            QMessageBox.warning(self, 'Warning', 'Passwords are not the same')
        else:
            if self.username.text() != '' and self.password.text() != '':
                try:
                    DBCtrl().add_user(name=self.username.text(), password=self.password.text())
                    super().accept()
                except IntegrityError:
                    QMessageBox.warning(self, 'Warning', 'This username is busy')
                except:
                    QMessageBox.warning(self, 'Warning', 'Something is wrong')


            else:
                QMessageBox.warning(self, 'Warning', 'Fill all fields')
