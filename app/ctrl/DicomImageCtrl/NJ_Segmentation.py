import os

import SimpleITK as sitk


class NJ_Segmentation:
    image: sitk.ImageFilter_5

    def __init__(self, img_path):
        self.image: sitk.Image = self.read_dicom_serie(img_path)
        self.spacing = self.image.GetSpacing()


    def make(self, point_1: list, point_2):
        process_image = self.__confidenceConneted(self.image, point_1[0], point_1[1], point_1[2])
        process_image1 = self.__confidenceConneted(self.image, point_2[0], point_2[1], point_2[2])
        process_image = self.__binaryDilated(process_image)
        process_image1 = self.__binaryDilated(process_image1)
        process_image = self.__fill(process_image)
        process_image1 = self.__fill(process_image1)
        process_image = self.__add_images(process_image, process_image1)
        process_image = self.make_binary(process_image)

        return process_image


    def make_binary(self, image):
        filter = sitk.BinaryThresholdImageFilter()
        filter.SetInsideValue(255)
        filter.SetOutsideValue(0)
        filter.SetLowerThreshold(1)
        filter.SetUpperThreshold(1)

        result = filter.Execute(image)

        return result


    def __confidenceConneted(self, image, x, y, z):
        filter = sitk.ConfidenceConnectedImageFilter()
        filter.SetInitialNeighborhoodRadius(8)
        filter.SetMultiplier(1.04)
        filter.SetSeed([x, y, z])
        result = filter.Execute(image)

        return result

    def __binaryDilated(self, image):
        spacing = [self.spacing[0] * 10, self.spacing[1] * 10, 0]

        filter = sitk.BinaryDilateImageFilter()
        filter.SetKernelRadius(int(self.spacing[0] * 10))
        filter.SetKernelType(sitk.BinaryDilateImageFilter.Ball)
        filter.SetBackgroundValue(0)
        filter.SetForegroundValue(1)
        result = filter.Execute(image)

        return result

    def __fill(self, image):
        filter = sitk.VotingBinaryIterativeHoleFillingImageFilter()
        filter.SetBackgroundValue(0)
        filter.SetForegroundValue(1)
        filter.SetRadius(2)
        filter.SetMaximumNumberOfIterations(1)
        result = filter.Execute(image)

        return result

    def __add_images(self, img1, img2):
        filter = sitk.AndImageFilter()
        result = filter.Execute(img1, img2)
        return result


    def read_img(self, path: str) -> sitk.Image:
        reader = sitk.ImageFileReader()
        filename, file_extension = os.path.splitext(path)
        jpgFormats = ['.jpg', '.JPG', '.jpeg', '.JPEG']
        bmpFormats = ['.bmp', '.BMP']
        pngFormats = ['.png', '.PNG']
        tifFormats = ['.tif', '.TIF', '.tiff', '.TIFF']

        if file_extension == '.dcm':
            reader.SetImageIO("GDCMImageIO")
        elif jpgFormats.count(file_extension) == 1:
            reader.SetImageIO("JPEGImageIO")
        elif bmpFormats.count(file_extension) == 1:
            reader.SetImageIO("BMPImageIO")
        elif pngFormats.count(file_extension) == 1:
            reader.SetImageIO("PNGImageIO")
        elif tifFormats.count(file_extension) == 1:
            reader.SetImageIO("TIFFImageIO")
        else:
            return None

        reader.SetFileName(path)
        image = reader.Execute()

        return image

    def read_dicom_serie(self, input):
        reader = sitk.ImageSeriesReader()

        dicom_names = reader.GetGDCMSeriesFileNames(input)
        reader.SetFileNames(dicom_names)

        self.image = reader.Execute()
        return self.image

    @staticmethod
    def save_image(image, output_path):
        sitk.WriteImage(image, output_path)


if __name__ == '__main__':
    img = NJ_Segmentation('C:/dicom/TCGA-LIHC/TCGA-BC-4073/02-21-2000-MRI ABD WWO CONT-85289/2.000000-NEW HASTE CORONAL-64499')
    seg = img.make([66, 78, 20], [85, 85, 16])
    img.save_image(seg, 'C:/dicom/output/eeee.nii')
