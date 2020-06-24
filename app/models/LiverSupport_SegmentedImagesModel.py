from __future__ import unicode_literals
from PySide2 import QtGui
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, QAbstractTableModel


class LiverSupport_SegmentedImagesModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(LiverSupport_SegmentedImagesModel, self).__init__()
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

            #missing un nessesary data
            if index.column() == (2 or 3 or 4):
                return

            key = self.colIndexToDictKey(index.column())
            if index.column() == 5:
                return str(self._data[index.row()][key])

            return self._data[index.row()][key]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return "SerieID"
            elif section == 5:
                return "Date upload"
            elif section == 6:
                return "State"

    def _col_width(self):
        col_width = 0
        data = self._data
        for row in zip(data):
            for col in row:
                for el in col:
                    if len(str(el)) > col_width:
                        col_width = len(str(el))

        return col_width + 5

    def colIndexToDictKey(self, index):
        if index == 0:
            return 'id'
        elif index == 1:
            return 'study_id'
        elif index == 2:
            return 'filepath_before'
        elif index == 3:
            return 'filepath_after'
        elif index == 4:
            return 'user_upload'
        elif index == 5:
            return 'date_upload'
        elif index == 6:
            return 'state'
