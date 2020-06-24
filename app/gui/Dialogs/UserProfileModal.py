from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QListView, QPushButton, QDialogButtonBox, QMessageBox, QLabel, QLineEdit
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QAbstractItemView
from app.ctrl.DatabaseCtrl import DBCtrl
from app.gui.Dialogs.RegisterDialog import RegisterDialog


class UserProfileModal(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.parent = parent
        self.setWindowTitle('Profile page')
        self.initUI()

    def initUI(self):
        usr = DBCtrl().get_user(self.parent.main_widget.username)
        usernameLabel = QLabel('Username:')
        self.username = QLabel(usr['username'])
        dateJoinLabel = QLabel('Date join:')
        join_date = QLabel(str(usr['include_date']))
        aetLabel = QLabel('PACS AET:')
        self.pacs_aet = QLineEdit(usr['aet'])
        portLabel = QLabel('PACS Port:')
        self.pacs_port = QLineEdit(usr['port'])
        adresLabel = QLabel('PACS Adres:')
        self.pacs_ip = QLineEdit(usr['adres_ip'])

        leftLayoutColumn = QVBoxLayout()
        leftLayoutColumn.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        leftLayoutColumn.addWidget(usernameLabel)
        leftLayoutColumn.addWidget(dateJoinLabel)
        leftLayoutColumn.addWidget(aetLabel)
        leftLayoutColumn.addWidget(adresLabel)
        leftLayoutColumn.addWidget(portLabel)

        rightLayoutColumn = QVBoxLayout()
        rightLayoutColumn.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        rightLayoutColumn.addWidget(self.username)
        rightLayoutColumn.addWidget(join_date)
        rightLayoutColumn.addWidget(self.pacs_aet)
        rightLayoutColumn.addWidget(self.pacs_ip)
        rightLayoutColumn.addWidget(self.pacs_port)

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
        layout.addWidget(self.buttons)

    def showWidget(self, parent=None):
        dialog = UserProfileModal(self.parent)
        ok = dialog.exec_()
        return ok

    def accept(self):
        DBCtrl().update_user(name=self.username.text(), aet=self.pacs_aet.text(),
                             port=self.pacs_port.text(), ip=self.pacs_ip.text())

        super().accept()
