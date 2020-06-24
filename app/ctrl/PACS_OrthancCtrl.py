import pyorthanc as po
from pyorthanc import Orthanc, Instance

from .PACS_ServerCtrl import PACS_ServerCtrl
from .SettingsCtrl import Config


class PACS_OrthancServerCtrl(PACS_ServerCtrl):
    def __init__(self):
        self.orthanc = Orthanc(Config.get('pacs_adres'))
        self.orthanc.setup_credentials(Config.get('pacs_login'), Config.get('pacs_password'))

    def isConnect(self) -> bool:
        return True

    def find(self):
        result = []
        patients_identifiers = self.orthanc.get_patients()
        for patient_identifier in patients_identifiers:
            patient_information = self.orthanc.get_patient_information(patient_identifier)
            id = patient_information['ID']
            patient_id = patient_information['MainDicomTags'].get('PatientID', '---')
            patient_name = patient_information['MainDicomTags'].get('PatientName', '---')
            patient_sex = patient_information['MainDicomTags'].get('PatientSex', '---')

            result.append([id, patient_id, patient_name, patient_sex])

        return result

    def find_study(self, patient_id):
        result = []
        patient_information = self.orthanc.get_patient_information(patient_id)
        study_identifiers = patient_information['Studies']

        for study_identifier in study_identifiers:
            study_information = self.orthanc.get_study_information(study_identifier)

            id = study_information['ID']
            study_date = study_information['MainDicomTags'].get('StudyDate', ' --- ')
            describe = study_information['MainDicomTags'].get('StudyDescription', '---')
            institution = study_information['MainDicomTags'].get('InstitutionName', '----')

            result.append([id, study_date, describe, institution])

        return result

    def find_series(self, study_id) -> list:
        result = []
        study_information = self.orthanc.get_study_information(study_id)
        series_identifiers = study_information['Series']
        for series_identifier in series_identifiers:
            series_information = self.orthanc.get_series_information(series_identifier)

            id = series_information['ID']
            modality = series_information['MainDicomTags'].get('Modality', '---')
            protocol = series_information['MainDicomTags'].get('ProtocolName', '---')
            imagesAmount = series_information['MainDicomTags'].get('ImagesInAcquisition', '---')

            result.append([id, modality, protocol, imagesAmount])
        return result

    def find_instance(self, series_id: str) -> list:
        result = []
        series_information = self.orthanc.get_series_information(series_id)
        instance_identifiers = series_information['Instances']
        for instance_identifier in instance_identifiers:
            instance_information = self.orthanc.get_instance_information(instance_identifier)
            result.append({'ID': instance_information['ID'],
                           'ParentSeries': instance_information['ParentSeries'],
                           'IndexInSeries': instance_information['IndexInSeries']})

        return result

    def move(self, instance_id: str, path: str):
        instance = Instance(instance_id, self.orthanc)
        dicom = instance.get_dicom_file_content()

        with open(path + '.dcm', 'wb+') as file_handler:
            file_handler.write(dicom)

    def store(self):
        pass
