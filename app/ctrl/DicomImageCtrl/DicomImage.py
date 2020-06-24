import glob
import os

import PIL
import pydicom
import numpy as np
from PIL.ImageQt import ImageQt
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QMessageBox

from app.ctrl.DicomImageCtrl.pydicom_PIL import get_PIL_image


class DicomImage:
    ''' Class handle all basic dicom images features '''
    __img3d: np.array
    __slice = pydicom.Dataset
    __slice_index: int = 0
    __slice_amount: int = 0
    __slices: list
    __shape: list
    __img_arr = None
    __x_scale: list = None
    __y_scale: list = None

    __ax_aspect: float
    __sag_aspect: float
    __cor_aspect: float

    __path: str
    __file_name: str

    def __init__(self, path: str = None):
        if path is not None:
            self.load_dicom(path)

    def load_dicom(self, path: str) -> None:
        if os.path.isfile(path):
            self.load_image(path)
        elif os.path.isdir(path):
            self.load_series(path)

    def load_image(self, path: str) -> None:
        try:
            image = pydicom.dcmread(path)
        except Exception:
            QMessageBox.warning(self, 'Problem', 'Unknown problem with dicom images... Contact with kkoziel@outlook.com')
        finally:
            self.__path = os.path.dirname(path)
            self.__slice = image
            self.__slices = self.__slice.pixel_array
            self.__slice_index = 0
            self.__slice_amount = 1
            self.__shape = list(self.__slice.pixel_array.shape)
            self.__shape.append(self.__slice_amount)
            self.__img3d = np.zeros(self.__shape)
            self.__img3d[:, :, 0] = self.__slice.pixel_array
            self.__img_arr = self.__img3d[:, :, 0]

    def load_series(self, dir_path):
        files = []
        for fname in glob.glob(dir_path + '*.dcm', recursive=False):
            files.append(pydicom.dcmread(fname))

        self.__path = dir_path

        # skip files with no SliceLocation (eg scout views)
        slices = []
        skipcount = 0
        for f in files:
            if hasattr(f, 'InstanceNumber'):
                slices.append(f)
            else:
                skipcount = skipcount + 1

        # ensure they are in the correct order
        slices = sorted(slices, key=lambda s: s.InstanceNumber)
        self.__slices = slices
        self.__slice_amount = len(slices)

        # pixel aspects, assuming all slices are the same
        # ps = slices[0].PixelSpacing
        # ss = slices[0].SliceThickness
        # ax_aspect = ps[1] / ps[0]
        # sag_aspect = ps[1] / ss
        # cor_aspect = ss / ps[0]

        # create 3D array
        self.__shape = list(slices[0].pixel_array.shape)
        self.__shape.append(len(slices))
        img3d = np.zeros(self.__shape)

        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            img2d = s.pixel_array
            img3d[:, :, i] = img2d

        self.__img3d = img3d
        self.__slice_index = 0
        self.__slice = self.__slices[self.__slice_index]
        self.__img_arr = self.__img3d[:, :, self.__slice_index]


    def slice(self) -> pydicom.Dataset:
        return self.__slice

    def get_slice_index(self) -> int:
        return self.__slice_index

    def get_slice_as_QImage(self) -> QImage:
        img = PIL.Image.fromarray(self.__img_arr)
        img = img.convert("L")
        result = ImageQt(img)

        return result

    def next_slice(self) -> None:
        if self.__slice_index < self.__slice_amount - 1 and self.is_series():
            self.__slice_index += 1
            self.__slice = self.__slices[self.__slice_index]
            self.__img_arr = self.__img3d[:, :, self.__slice_index]

    def pre_slice(self) -> None:
        if self.__slice_index > 0 and self.is_series():
            self.__slice_index -= 1
            self.__slice = self.__slices[self.__slice_index]
            self.__img_arr = self.__img3d[:, :, self.__slice_index]

    def set_slice_index(self, index: int):
        self.__slice_index = index
        self.__slice = self.__slices[self.__slice_index]
        self.__img_arr = self.__img3d[:, :, self.__slice_index]

    def is_last_slice(self) -> bool:
        if self.is_image() or self.__slice_index == self.__slice_amount - 1:
            return True
        return False

    def is_first_slice(self) -> bool:
        if self.is_image() or self.__slice_index == 0:
            return True
        return False

    def is_series(self) -> bool:
        if self.__slice_amount != 1:
            return True
        return False

    def is_image(self) -> bool:
        if self.__slice_amount == 1:
            return True
        return False

    def is_data_load(self) -> bool:
        if self.__slice_amount == 0:
            return False
        return True

    def get_slice_amount(self) -> int:
        if self.is_data_load():
            return self.__slice_amount
        return 0

    def get_shape(self):
        return self.__shape

    def get_study_id(self):
        return self.__slice["StudyID"]

    @staticmethod
    def read(path: str) -> pydicom.Dataset:
        dicom = pydicom.dcmread(path)
        return dicom

    @staticmethod
    def toQImage(img: pydicom.Dataset):
        result = get_PIL_image(img)
        result = ImageQt(result)

        return result

    @property
    def dicom_dir(self):
        return self.__path

    @dicom_dir.setter
    def dicom_dir(self, dir_path: str):
        self.__path = dir_path

    @property
    def filename(self):
        return self.__file_name
