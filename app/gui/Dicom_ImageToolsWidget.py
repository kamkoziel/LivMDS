from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableView, QVBoxLayout, QLabel, QPushButton, QColorDialog, QSlider, \
    QDoubleSpinBox

from app.gui.ColorButton import ColorButton


class Dicom_ImageToolsWidget(QWidget):
    __tab_name__ = 'Tools'
    pen_selected = Signal()
    mask_color: QColor() = QColor('green')
    pen: bool = False

    def __init__(self):
        super().__init__()
        self.width = 20
        self.init_ui()

    def init_ui(self):

        self.slider = self.__init_slider__()
        self.color_btn = ColorButton(self.mask_color)
        self.color_btn.clicked.connect(self.open_color_dialog)
        self.pen_btn = QPushButton('Pen')

        self.pen_size = QDoubleSpinBox()
        self.pen_size.setRange(1, 30)
        self.pen_size.setValue(1)
        self.pen_size.setDecimals(0)
        self.pen_size.setSingleStep(1)
        self.pen_btn.setCheckable(True)
        self.pen_btn.clicked.connect(self.pen_selected.emit)

        self.erase_btn = QPushButton('Erase')
        self.erase_btn.setCheckable(True)

        self.processing_btn = QPushButton('Segment with NN')
        self.nj_segment_btn = QPushButton('Semi automated segment')

        self.load_mask_btn = QPushButton('Load mask from NIFTI')
        self.save_mask_btn = QPushButton('Save mask to NIFTI')

        self.scope_btn = QPushButton('Scope')

        drawing_layout = QHBoxLayout()
        drawing_layout.addWidget(self.pen_btn)
        drawing_layout.addWidget(self.erase_btn)

        segmentation_layout = QHBoxLayout()
        segmentation_layout.addWidget(self.processing_btn)
        segmentation_layout.addWidget(self.nj_segment_btn)

        files_managment_layout = QHBoxLayout()
        files_managment_layout.addWidget(self.load_mask_btn)
        files_managment_layout.addWidget(self.save_mask_btn)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(QLabel('Image slice: '))
        layout.addWidget(self.slider)
        layout.addWidget(QLabel('Mask color: '))
        layout.addWidget(self.color_btn)
        layout.addWidget(self.pen_size)
        layout.addLayout(drawing_layout)
        layout.addLayout(segmentation_layout)
        layout.addLayout(files_managment_layout)

    def open_color_dialog(self):
        self.mask_color = QColorDialog.getColor(self.color_btn.color)
        self.color_btn.color = self.mask_color
        self.color_btn.update()

    def get_color(self) -> QColor: return self.mask_color

    def get_size(self) -> int: return int(self.pen_size.value())

    def set_slider_maximum(self, max: int):
        self.slider.setMaximum(max)

    @property
    def tab_name(self):
        return self.__tab_name__

    def __init_slider__(self, max: int = 1) -> QSlider:
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(max)
        slider.setTickInterval(1)
        slider.setSliderPosition(1)

        return slider
