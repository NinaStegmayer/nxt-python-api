from nxt_rest_connection import NXTRestConnection
from utils.dto.rest_result import RestResult
from utils.dto.roi_object import RoiObject


class NxtHandler:

    def __init__(self, ip, username, password):
        # SSL Connection seems to be sometimes unstable
        self.rest_connection = NXTRestConnection(ip, username, password, False)

    # jetzt im CameraHandler
    # def get_device_info(self) -> RestResult:
    #     return self.rest_connection.get('/deviceinfo')

    # im CameraHandler
    # def get_trigger_settings(self) -> RestResult:
    #     return self.rest_connection.get('/camera/trigger')

    # im CameraHandler
    # def set_camera_trigger_to_software(self) -> RestResult:
    #     params = {'TriggerType': 'Software'}
    #     return self.rest_connection.patch("/camera/trigger", params=params)

    # im CameraHandler
    # def trigger(self):
    #     return self.rest_connection.post("/camera/trigger")

    # im CameraHandler
    # def get_sensor_roi(self) -> RoiObject:
    #     return RoiObject.from_json(self.rest_connection.get("/camera/roi").to_json())

    # im AppHandler
    # def get_vapps_installed(self) -> [str]:
    #     vapp_object = self.rest_connection.get(f'/vapps/').to_json()
    #     return vapp_object["Installed"]

    # im AppHandler
    # def get_vapps_running(self) -> [str]:
    #     running_vapps = []
    #     installed_vapps = self.get_vapps_installed()
    #
    #     for vapp in installed_vapps:
    #         vapp_status = self.rest_connection.get(f'/vapps/{vapp}').to_json()["Status"]
    #         if vapp_status == "Running":
    #             running_vapps.append(vapp)
    #
    #     return running_vapps

    # im CameraHandler
    # def get_camera_image_latest(self, filename: str):
    #
    #     image_header = NxtRestConnection.get_image_accept_header_by_filename(filename)
    #     header = {'Accept': image_header.value}
    #     params = {'quality': 80}
    #
    #     result = self.rest_connection.get(f'/camera/image', params=params, additional_headers=header)
    #     with open(filename, 'wb') as file:
    #         file.write(result.get_response_data())

    # im CameraHandler
    # def set_test_image(self, filename: str):
    #     image_header = NxtRestConnection.get_image_accept_header_by_filename(filename)
    #     content_type = NxtRestConnection.get_image_content_type_by_filename(filename)
    #     header = {'Accept': image_header.value}
    #
    #     file = open(filename, "rb").read()
    #
    #     return self.rest_connection.put(f'/camera/image/testimage/custom', content_type=content_type, data=file,
    #                                     additional_headers=header)

    # def install_vapp(self, filepath: str, vapp: str):
    #     header = {'Accept': '*/*'}
    #     content_type = NxtRestConnection.HttpContentTypes.ApplicationVapp
    #     with open(filepath, 'rb') as data:
    #         self.rest_connection.put(f'/vapps/{vapp}', content_type=content_type, additional_headers=header,
    #                                  data=data.read())
    #
    # def activate_vapp(self, vapp: str):
    #     header = {'Accept': '*/*'}
    #     self.rest_connection.put(f'/vapps/activated/{vapp}', additional_headers=header)
    #
    # def deactivate_vapp(self, vapp: str):
    #     header = {'Accept': '*/*'}
    #     self.rest_connection.delete(f'/vapps/activated/{vapp}', additional_headers=header)
    #
    # def deactivate_running_vapps(self):
    #     for app in self.get_vapps_running():
    #         self.deactivate_vapp(app)
    #
    # def delete_vapp(self, vapp: str):
    #     header = {'Accept': '*/*'}
    #     content_type = NxtRestConnection.HttpContentTypes.ApplicationVapp
    #     self.rest_connection.delete(f'/vapps/{vapp}', content_type=content_type, additional_headers=header)

    # im CameraHandler
    # def delete_test_image(self):
    #     return self.rest_connection.delete(f'/camera/image/testimage/custom')
