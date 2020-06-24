from PySide2 import QtGui
from PySide2.QtCore import Qt, QMargins
from PySide2.QtWidgets import QMainWindow

from app.ctrl.Utils import get_style
from app.gui.MainWidget import MainWidget
from app.gui.Menus.MenuBar import MenuBar


class App(QMainWindow):
    style_path = 'res/styles/main_window_style.css'

    def __init__(self, user: str):
        super().__init__()
        self.user = user

        self.title = 'LiverMDS'

        self.initUI()

    def initUI(self):
        main_widget = MainWidget(self)
        menu_bar = MenuBar(main_widget)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setWindowIcon(QtGui.QIcon('img/DPC.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 1200, 800)
        self.setStyleSheet(get_style(self.style_path))
        self.setMenuBar(menu_bar)
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(main_widget)

        self.show()
