# This Python file uses the following encoding: utf-8
import os
import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication

from app.ctrl.Utils import get_app_dir, start_app
from app.gui.Dialogs.LoginDialog import LoginDialog
from app.gui.Dialogs.SettingsDialog import SettingDialog
from app.gui.MainWindow import App
from app.ctrl.SettingsCtrl import Config


if __name__ == '__main__':
    Config.update('app_dir', get_app_dir())
    start_app()

    app = QApplication(sys.argv)

    if not Config.get('dont_show_settings_startup'):
        sett = SettingDialog()
        sett.show()
        sett.exec_()

    # With Login
    login = LoginDialog()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        ex = App(login.username_auth())
        sys.exit(app.exec_())

    # Without login
    # ex = App('kkozi')
    # sys.exit(app.exec_())
