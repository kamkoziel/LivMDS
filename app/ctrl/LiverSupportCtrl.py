from app.ctrl.DatabaseCtrl import DBCtrl


class LiverSupportCtrl:
    def get_images(self):
        images_dict = DBCtrl().get_images_process()

        return images_dict