from __future__ import unicode_literals
from PySide2 import QtGui
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, QAbstractTableModel

tick = QtGui.QImage('res/img/icons/activeUsr_32.png')


class PACS_SeriesTabModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(PACS_SeriesTabModel, self).__init__()
        self._data = data

    def update(self, data):
        self._data = data
        self.max_length = self._col_width()

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return "Modality"
            elif section == 2:
                return "Instance"
            elif section == 3:
                return "ImagesAmount"

    def _col_width(self):
        col_width = 0
        data = self._data
        for row in zip(data):
            for col in row:
                for el in col:
                    if len(str(el)) > col_width:
                        col_width = len(str(el))

        return col_width + 5
