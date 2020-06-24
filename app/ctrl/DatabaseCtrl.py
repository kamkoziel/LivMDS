from datetime import datetime
from typing import Dict, Any, Union

from app.ctrl.SettingsCtrl import Config
from app.models.DatabaseModel import base
from sqlalchemy import create_engine


def select_to_dict(select_response):
    result_list = []
    result = {}
    for rowproxy in select_response:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            result = {**result, **{column: value}}
        result_list.append(result)

    if len(result_list) == 1:
        return result_list[0]

    return result_list


class DBCtrl:
    def __init__(self, user: str = Config.get('db_user'), password: str = Config.get('db_password'), host: str = Config.get('db_host'),
                 db_name: str = Config.get('db_name')):
        self.__db_string__ = 'postgresql+psycopg2://' + user + ':' + password + '@' + host + '/' + db_name
        self.db = self.__make_connect()
        self.__create_tables()


    def __make_connect(self):
        db = create_engine(self.__db_string__)
        return db

    def __create_tables(self):
        # base.metadata.drop_all(self.db)
        base.metadata.create_all(self.db)

    # Users
    def add_user(self, name: str, password: str):
        time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("INSERT INTO users (name, password, is_activ, include_date) VALUES ('{0}', '{1}', FALSE, '{2}')"
                        .format(name, password, time_now))

    def is_user(self, name: str, password: str, ):
        result_set = self.db.execute("SELECT * FROM users WHERE name='{0}' AND password='{1}'".format(name, password))
        user_data = {}
        try:
            user_data = select_to_dict(result_set)

        finally:
            if len(user_data):
                return True, user_data
            else:
                return False, []

    def get_user(self, username) -> Dict[str, Union[str, Any]]:
        result = self.db.execute(
            "SELECT * FROM users WHERE name='{0}'".format(username))
        row = result.first()
        username = row[1]
        aet = str(row[3])
        adr_ip = str(row[4])
        port = str(row[5])
        include_date = str(row[6])

        return {'username': username,
                'aet': aet,
                'adres_ip': adr_ip,
                'port': port,
                'include_date': include_date}

    def update_user(self, name: str, aet: str, port: int, ip: str):
        self.db.execute(" UPDATE users SET aet = '{1}', port = {2}, adres_ip = '{3}' WHERE name = '{0}'"
                        .format(name, aet, port, ip))

    def add_archive(self, aec: str, port: int = None, description: str = None, adres_ip: str = None):
        self.db.execute(
            "INSERT INTO archives (aec, adres_ip, port, description, is_activ) VALUES ('{0}', '{1}', {2}, '{3}', TRUE)"
                .format(aec, adres_ip, port, description))

    # SESSION
    def open_session(self, user_id):
        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("INSERT INTO user_session (start_time, user_id) VALUES ('{0}', '{1}')"
                        .format(time, user_id))
        response = self.db.execute(
            "SELECT * FROM user_session WHERE start_time='{0}' AND user_id='{1}'".format(time, user_id))

        result = select_to_dict(response)

        return result

    # IMAGE PROCESSING
    def add_image_process(self, study_id, user_id):
        time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute(
            "INSERT INTO nn_processing (study_id, user_upload, state, date_upload) VALUES ('{0}', '{1}', 'wait', '{2}')".format(
                study_id, user_id, time_now))

    def update_image_process(self, study_id, state='ready'):
        self.db.execute(
            "UPDATE nn_processing SET state = '{1}' WHERE study_id = '{0}'".format(study_id, state))

    def image_procesing_state(self, study_id):
        result = self.db.execute(
            "SELECT * FROM nn_processing WHERE study_id='{0}'".format(study_id))

        result = select_to_dict(result)

    def get_images_process(self):
        response = self.db.execute("SELECT * FROM nn_processing ")
        result = select_to_dict(response)
        return result
