from enum import Enum


class PACS_Stage(Enum):
    PATIENT = 0
    STUDY = 1
    SERIES = 2
    INSTANCE = 3