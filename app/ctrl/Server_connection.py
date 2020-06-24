import os
import socket

from app.ctrl.SettingsCtrl import Config

TCP_IP = '192.168.0.113'
TCP_PORT = 9001
BUFFER_SIZE = 1024


def open_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    return s


class Client_order():
    @staticmethod
    def get_segmented(study_id, files_path='/data/.segmented_nn_images/'):
        s = open_connection()
        order = 'GIVE ' + study_id
        s.send(order.encode())
        recv = s.recv(BUFFER_SIZE)
        if recv.decode() == 'SENDING':
            path = files_path
            is_dir = os.path.isdir(path)
            if not is_dir:
                os.mkdir(path)
            path = path + study_id + '_nn_segmented.nii'

            with open(path, 'wb') as f:
                while True:
                    data = s.recv(BUFFER_SIZE)
                    if not data:
                        f.close()

                        break
                    # write data to a file
                    f.write(data)
            s.close()

        elif recv.decode() == 'LACK OF ARGS':
            return
        else:
            s.close()


    @staticmethod
    def send_segmented(series_name):
        s = open_connection()
        s.send('GET {0}'.format(series_name).encode())
        file_path = Config.get('app_dir') + '/data/.segemented_images/test-segmentation-0.nii'
        if os.path.exists(file_path):
            file = open(file_path, 'rb')
            while True:
                pack = file.read(BUFFER_SIZE)
                s.send(pack)
                if not pack:
                    file.close()
                    s.close()
                    break
        else:
            s.close()


if __name__ == '__main__':
    Client_order.get_segmented('c11eb7f8-eba89e44-c6541b0c-eb4d651b-ea8c26a6')
