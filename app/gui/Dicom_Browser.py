import os

import PIL
import numpy as np
from PIL.ImageQt import ImageQt
from PySide2.QtCore import Qt, QRect, QSize, QPoint, QProcess, Signal
from PySide2.QtGui import QPixmap, QPainter, QPen, QImage, QBitmap, QCursor
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QTabWidget, QSplitter, QRubberBand, QSlider, \
    QVBoxLayout, QGroupBox, QApplication

from app.ctrl.Dicom_BrowserCtrl import Dicom_BrowserCtrl
from app.ctrl.DicomImageCtrl.DicomImage import DicomImage
from app.gui.Dicom_ImageToolsWidget import Dicom_ImageToolsWidget
from app.gui.Dicom_Tags_Widget import Dicom_Tags_Widget


class Dicom_Browser(QWidget):
    draw_state: bool = False
    erase_state: bool = False
    point_pick: bool = False
    nj_points = []
    nj_points_ready = Signal()
    series_id: str
    mask: np.array

    def __init__(self):
        super().__init__()
        self.initUI()
        self.rubberBand: QRubberBand = QRubberBand(QRubberBand.Line, self.image_label)

    def initUI(self):
        self.image = DicomImage()
        self.pixmap = QPixmap()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.image_label.setPixmap(self.pixmap)

        self.tags_view = Dicom_Tags_Widget([''])
        self.tools = Dicom_ImageToolsWidget()

        self.tabs_widget = self.__inti_tab_widget__([self.tags_view, self.tools])
        self.tabs_widget.setMaximumWidth(600)

        image_layout = QVBoxLayout()
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.addWidget(self.image_label)

        image_group = QGroupBox()
        image_group.setStyleSheet("margin:0; padding: 0; border: 0;")
        image_group.setContentsMargins(0, 0, 0, 0)
        image_group.setLayout(image_layout)

        splitter = QSplitter()
        splitter.addWidget(image_group)
        splitter.addWidget(self.tabs_widget)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

        self.tools.pen_selected.connect(self.pen_select)
        self.tools.erase_btn.clicked.connect(self.erase_btn_click)
        self.tools.slider.valueChanged.connect(self.slider_changed)
        self.tools.processing_btn.clicked.connect(self.send_nn_segmentation)
        self.tools.load_mask_btn.clicked.connect(self.load_nifti_mask_click)
        self.tools.save_mask_btn.clicked.connect(self.save_nifti_mask_click)
        self.tools.nj_segment_btn.clicked.connect(self.nj_segment_click)
        self.nj_points_ready.connect(self.nj_segment)

    def set_image(self):
        self.pixmap = QPixmap.fromImage(self.image.get_slice_as_QImage())
        self.image_label.setPixmap(self.pixmap)
        self.set_tags()

    def update_mask(self):
        self.mask = np.zeros([self.image.get_shape()[0], self.image.get_shape()[1], self.image.get_slice_amount()],
                             np.int)
        self.draw_mask()

    def load_series(self, path):
        if isinstance(path, list):
            if len(path) == 1:
                path = path[0]
            else:
                path = os.path.dirname(path[0]) + '/'

        self.image.load_dicom(path)
        self.set_image()
        if self.image.is_series():
            self.set_slider_maximum()
            self.tools.slider.setDisabled(False)
        else:
            self.tools.slider.setDisabled(True)
        self.set_tags()
        self.update_tags()
        self.update_mask()

    def set_tags(self):
        result = []
        for elem in self.image.slice().iterall():
            result.append([str(elem.tag), elem.name, str(elem.value)])

        return result

    def update_tags(self):
        self.tags_view.model.update(self.set_tags())
        self.tags_view.model.layoutChanged.emit()

    # MOUSE EVENTS

    def wheelEvent(self, event):

        if self.image_label.underMouse():
            delta = event.delta()
            if delta > 0:
                self.image.next_slice()
            elif delta < 0:
                self.image.pre_slice()

            self.set_image()
            self.tools.slider.setSliderPosition(self.image.get_slice_index())
            self.update_tags()
            self.draw_mask()
            self.update()

    def mousePressEvent(self, e):
        if self.image_label.underMouse():
            if self.draw_state:
                self.pos = self.point_on_image(e)
                self.set_mask_pixels(self.pos)
                self.draw_mask_point(self.pos)
                self.update()
            elif self.erase_state:
                self.pos = self.point_on_image(e)
                self.set_mask_pixels(self.pos, 0)
                self.set_image()
                self.draw_mask()
                self.update()
            elif self.point_pick:
                point = [self.point_on_image(e).x(), self.point_on_image(e).x(), self.image.get_slice_index()]
                self.nj_points.append(point)
                if len(self.nj_points) == 2:
                    self.point_pick = False
                    QApplication.restoreOverrideCursor()
                    self.nj_points_ready.emit()
            else:
                self.origin = e.pos()
                if not self.rubberBand:
                    self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()

    def mouseMoveEvent(self, e):
        if self.image_label.underMouse():
            if self.draw_state:
                self.pos = self.point_on_image(e)
                self.set_mask_pixels(self.pos)
                # self.mask[int(self.pos.y())][int(self.pos.x())][self.image.get_slice_index()] = 255
                self.draw_mask_point(self.pos)
                self.update()
            elif self.erase_state:
                self.pos = self.point_on_image(e)
                self.set_mask_pixels(self.pos, 0)
                # self.mask[int(self.pos.y())][int(self.pos.x())][self.image.get_slice_index()] = 0
                self.set_image()
                self.draw_mask()
                self.update()
            else:
                self.rubberBand.setGeometry(QRect(self.origin, e.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if self.image_label.underMouse():
            if self.draw_state:
                return
            self.rubberBand.hide()

    def keyPressEvent(self, event):
        # Re-direct ESC key to closeEvent
        if event.key() == Qt.Key_Escape:
            if self.point_pick:
                self.point_pick = not self.point_pick
                QApplication.restoreOverrideCursor()

    # IMAGE SLIDER

    def set_slider_maximum(self):
        self.tools.set_slider_maximum(self.image.get_slice_amount() - 1)

    def slider_changed(self):
        self.image.set_slice_index(self.tools.slider.value())
        self.set_image()
        self.update_tags()
        self.draw_mask()
        self.update()

    def pen_select(self):
        self.draw_state = self.tools.pen_btn.isChecked()

    def __init_slider(self) -> QSlider:
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setMaximumWidth(self.image_label.width())
        slider.setMinimum(0)
        slider.setMaximum(self.image.get_slice_amount())
        slider.setTickInterval(1)
        slider.setSliderPosition(1)
        slider.valueChanged.connect(self.slider_changed)
        if not self.image.is_series():
            slider.setHidden(True)

        return slider

    def __inti_tab_widget__(self, widgets: list) -> object:
        tabs_widget = QTabWidget()
        tabs_widget.setTabPosition(QTabWidget.South)
        tabs_widget.setMinimumWidth(50)
        for wdg in widgets:
            tabs_widget.addTab(wdg, wdg.tab_name)

        return tabs_widget

    # MASKING
    def send_nn_segmentation(self):
        # Dicom_BrowserCtrl.save_mask(self, self.mask, 'res/H-DenseUNet-master_v1/livermask/0.nii')
        ctrl = Dicom_BrowserCtrl()
        head, tail = os.path.split(os.path.split(self.image.dicom_dir)[0])
        ctrl.image_to_nn(tail, self.mask, self.image.get_shape()[0], self.image.get_shape()[1])

    def set_mask(self):
        img = self.__arr_to_QImage(self.mask[:, :, self.image.get_slice_index()].T())
        self.mask_pixmap = QPixmap.fromImage(img)
        self.mask_label.setPixmap(self.mask_pixmap)

    def draw_mask(self):
        try:
            if not np.array_equal(self.mask[:, :, self.image.get_slice_index()],
                                  np.zeros([self.image.get_shape()[0], self.image.get_shape()[1]])):
                it = np.nditer(self.mask[:, :, self.image.get_slice_index()], flags=['multi_index'])
                for pixel in it:
                    if pixel != 0:
                        point = QPoint(it.multi_index[1], it.multi_index[0])
                        self.draw_mask_point(point, 1)
        except Exception:
            self.update_mask()


    def set_mask_pixels(self, center_point: QPoint, value=255):
        it = np.nditer(self.mask[:, :, self.image.get_slice_index()], flags=['multi_index'])
        size = int(self.tools.get_size() / 2) - 1
        x = center_point.x()
        y = center_point.y()
        for pixel in it:
            if x - size <= it.multi_index[1] <= x + size and y + size >= it.multi_index[0] >= y - size:
                self.mask[it.multi_index[0]][it.multi_index[1]][self.image.get_slice_index()] = value

    def draw_mask_point(self, point, pen_size: int = None):
        if pen_size is None:
            pen_size = self.tools.get_size()
        painter = QPainter(self.image_label.pixmap())
        painter.setPen(QPen(self.tools.mask_color, pen_size, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
        painter.drawPoint(point)

    def erase_btn_click(self):
        self.erase_state = not self.erase_state
        self.tools.erase_btn.setChecked(self.erase_state)
        if self.draw_state:
            self.draw_state = not self.draw_state
            self.tools.pen_btn.setChecked(self.draw_state)

    def load_nifti_mask_click(self):
        ctrl = Dicom_BrowserCtrl()
        self.mask = ctrl.load_nitfit_mask()
        self.draw_mask()
        self.update()

    def save_nifti_mask_click(self):
        Dicom_BrowserCtrl.save_mask(self, self.mask)

    def nj_segment_click(self):
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.point_pick = True

    def nj_segment(self):
        ctrl = Dicom_BrowserCtrl()
        ctrl.nj_segment(self.image.dicom_dir, self.nj_points)
        self.nj_points = []
        self.mask = ctrl.load_nitfit_mask('data/.tmp.nii')
        self.draw_mask()
        self.update()

    def point_on_image(self, e):
        x_offset, y_offset = self.__image_offset()
        pos = QPoint(e.x() - x_offset, e.y() - y_offset)

        return pos

    def __image_offset(self):
        x_offset = (self.image_label.width() - self.pixmap.width()) / 2
        y_offset = (self.image_label.height() - self.pixmap.height()) / 2
        return x_offset, y_offset

    def __arr_to_QImage(self, arr_img):
        img = PIL.Image.fromarray(arr_img)
        img = img.convert("L")
        result = ImageQt(img)

        return result
