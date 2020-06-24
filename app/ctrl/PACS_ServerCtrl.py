from abc import ABC

class PACS_ServerCtrl(ABC):
    def isConnect(self) -> bool:
        pass

    def find(self)-> list:
        pass

    def move(self, instance_id: str, path: str):
        pass

    def store(self):
        pass

    def find_patients(self):
        pass

    def find_study(self, patient_id) -> list:
        pass

    def find_series(self, param):
        pass

    def find_instance(self, param):
        pass