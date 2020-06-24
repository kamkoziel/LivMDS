from PySide2.QtCore import QRect
from PySide2.QtGui import QPainter, QBrush, Qt, QColor
from PySide2.QtWidgets import QPushButton


class ColorButton(QPushButton):
    def __init__(self, color: QColor = QColor('green')):
        super().__init__()
        self.color = color

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(3, 3, -6 + self.width(), -6 + painter.device().height())
        painter.setBrush(brush)
        painter.fillRect(rect, brush)
