from PySide2.QtWidgets import QTableView, QHeaderView, QAbstractScrollArea


class PACSItemView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent=parent)
        self.activeImage: str = None

        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setMinimumWidth(200)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.resizeColumnsToContents()
