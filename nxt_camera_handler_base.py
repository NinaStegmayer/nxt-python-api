from enum import Enum

from utils.dto.camera_roi import CameraRoi
from nxt_rest_connection import NXTRestConnection
from utils.dto.rest_result import RestResult
from utils.settings.camera_settings_base import CameraSettingsBase
from utils.settings.color_settings_base import ColorSettingsBase
from utils.settings.trigger_settings_base import TriggerSettingsBase


class NXTCameraHandlerBase:
    """
    Provides functions to set / get camera, color , trigger, roi settings.

    Is inherited from NXTRioCameraHandler and NXTMalibuCameraHandler.

    Requires an established NXTRestConnection.

    Note: color settings only available on color sensors"""

    def __init__(self, rest_connection: NXTRestConnection):
        # SSL Connection seems to be sometimes unstable
        self.rest_connection = rest_connection
        self.camera_setting_class = CameraSettingsBase()
        self.color_setting_class = ColorSettingsBase()
        self.trigger_setting_class = TriggerSettingsBase()

    def get_device_info(self) -> RestResult:
        """Returns the device information like device model, device type, device name, etc."""
        return self.rest_connection.get('/deviceinfo')

    def get_minimum(self, node_path: str, setting: str):
        """Returns the minimum value of the given setting. Uses the OPTIONS request on the given node."""
        options = self.rest_connection.options(node_path).to_json()
        return options["GET"]["application/json"]["Values"][setting]["Range"]["Minimum"]



    def get_camera_settings_ranges(self, settings: [str]) -> dict:
        ranges = {}
        options = self.rest_connection.options('/camera').to_json()
        for setting in settings:
            ranges[setting] = options["GET"]["application/json"]["Values"][setting]["Range"]
        return ranges

    def get_camera_settings_options(self):
        return self.rest_connection.options('/camera').to_json()["GET"]["application/json"]["Values"]

    def set_camera_setting(self, setting: str, value: int | str | bool | float):
        param = {setting: value}
        return self.rest_connection.patch('/camera', content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=param)

    def get_color_settings(self) -> ColorSettingsBase:
        return self.color_setting_class.from_json(self.rest_connection.get('/camera/color',
                                                                           content_type=NXTRestConnection.
                                                                           HttpContentTypes.ApplicationJson).to_json())

    def get_custom_color_settings(self, color_settings: [str]):
        """existing color settings: BlueGain / GreenGain / RedGain / WhiteBalance"""
        setting_dict = {}
        values = self.rest_connection.get('/camera/color',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()
        for setting in color_settings:
            setting_dict[setting] = values[setting]
        return setting_dict

    def set_color_setting(self, color_setting: str, value: float | str):
        """existing color settings: BlueGain: float [0-100] / GreenGain: float [0-100] / RedGain: float [0-100]/
        WhiteBalance: str [Off / Continuous / Once]"""
        param = {color_setting: value}
        return self.rest_connection.patch('/camera/color',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=param)

    def get_color_settings_options(self):
        return self.rest_connection.options('/camera/color').to_json()["GET"]["application/json"]

    def get_color_correction_options(self):
        return self.rest_connection.options('/camera/color/colorcorrection').to_json()["GET"]["application/json"]

    def get_color_correction_settings(self):
        return self.rest_connection.get('/camera/color/colorcorrection',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()

    def get_custom_color_correction_settings(self, color_correction_settings: [str]):
        """existing color correction settings: ColorCorrectionMatrixType / ColorCorrectionMode"""
        setting_dict = {}
        values = self.rest_connection.get('/camera/color/colorcorrection',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()
        for setting in color_correction_settings:
            setting_dict[setting] = values[setting]
        return setting_dict

    def set_color_correction_setting(self, color_correction_setting: str, value: str):
        """existing color correction settings: ColorCorrectionMatrixType / ColorCorrectionMode"""
        param = {color_correction_setting: value}
        return self.rest_connection.patch('/camera/color/colorcorrection',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=param)

    def set_color_correction_settings(self, color_correction_settings: dict):
        """existing color correction settings: ColorCorrectionMatrixType / ColorCorrectionMode"""
        return self.rest_connection.patch('/camera/color/colorcorrection',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=color_correction_settings)

    def get_colorcorrection_matrix_options(self):
        return self.rest_connection.options('/camera/color/colorcorrection/matrix').to_json()["GET"]["application/json"]

    def get_colorcorrection_matrix(self):
        return self.rest_connection.get('/camera/color/colorcorrection/matrix',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()

    def get_colorcorrection_matrix_custom_value(self, gains: [str]):
        """Gain00: red contribution to the red pixel/ Gain01: green contribution to the red pixel/ Gain02: blue contribution to the red pixel
Gain10: red contribution to the green pixel/Gain11: green contribution to the green pixel/Gain12: blue contribution to the green pixel
Gain20: red contribution to the blue pixel/Gain21: green contribution to the blue pixel/Gain22: blue contribution to the blue pixel"""
        matrix_dict = {}
        values = self.rest_connection.get('/camera/color/colorcorrection/matrix',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()
        for gain in gains:
            matrix_dict[gain] = values[gain]
        return matrix_dict

    def set_colorcorrection_matrix(self, matrix_values: dict):
        """NOTE: CAN ONLY BE SET IF ColorCorrectionMatrixType IS SET TO Custom0!
         Gain00: red contribution to the red pixel/ Gain01: green contribution to the red pixel/ Gain02: blue contribution to the red pixel
        Gain10: red contribution to the green pixel/Gain11: green contribution to the green pixel/Gain12: blue contribution to the green pixel
        Gain20: red contribution to the blue pixel/Gain21: green contribution to the blue pixel/Gain22: blue contribution to the blue pixel"""
        header = {'Accept': '*/*'}
        return self.rest_connection.patch('/camera/color/colorcorrection/matrix',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationXWwwFormUrlencoded,
                                          params=matrix_values, additional_headers=header)

    def get_image_options(self):
        return self.rest_connection.options('/camera/image').to_json()["GET"]

    def save_camera_image_latest(self, filename: str):
        """Note: requires some time to generate image"""

        image_header = NXTRestConnection.get_image_accept_header_by_filename(filename)
        header = {'Accept': image_header.value}
        params = {'quality': 80}

        result = self.rest_connection.get(f'/camera/image', params=params, additional_headers=header)
        with open(filename, 'wb') as file:
            file.write(result.get_response_data())

    def get_camera_test_image_latest_options(self):
        return self.rest_connection.options('/camera/image/testimage').to_json()["GET"]["application/json"]

    def get_camera_test_image_setting(self):
        return self.rest_connection.get('/camera/image/testimage',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()

    class TESTPATTERN(Enum):
        OFF = "Off"
        VERTICAL_WEDGE = "VerticalWedge"
        HORIZONTAL_WEDGE = "HorizontalWedge"
        WHITE = "White"
        BLACK = "Black"
        GRAYSCALE = "Grayscale"
        CHECKERBOARD = "Checkerboard"
        GREYDIAGONALRAMPMOVING = "GreyDiagonalRampMoving"
        SEQUENZPATTERN1 = "SequencePattern1"
        SEQUENZPATTERN2 = "SequencePattern2"
        FRAMECOUNT = "Framecount"
        COLORSTRIPE = "ColorStripe"

    def set_camera_image_testpattern(self, test_pattern: TESTPATTERN):
        header = {'Accept': '*/*'}
        param = {'Testpattern': test_pattern.value}
        return self.rest_connection.patch('/camera/image/testimage',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationXWwwFormUrlencoded,
                                          params=param, additional_headers=header)

    def get_camera_testimage_custom_options(self):
        return self.rest_connection.options('/camera/image/testimage/custom').to_json()

    def get_camera_testimage_custom(self):
        """Returns the information about the custom test image mode."""
        return self.rest_connection.get('/camera/image/testimage/custom',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()

    def delete_camera_testimage_custom(self):
        header = {'Accept': '*/*'}
        return self.rest_connection.delete('/camera/image/testimage/custom', additional_headers=header)

    def set_test_image(self, filename: str):
        """Uploads and enables a custom test image.

        The maximum size of the test image is 25 MB. Allowed image formats are JPEG, PNG and BMP.
        After uploading, the test image is activated automatically. Image acquisition continues in the background.
        The test image is deleted when the camera is restarted.
        If a sensor ROI is set (change of image height or image width) the test image will be scaled accordingly.
        Functions such as gamma or binning do not have any effect on the test image.
        Uploading a test image again overwrites an existing test image.
        The test image is not included in a camera backup."""

        image_header = NXTRestConnection.get_image_accept_header_by_filename(filename)
        content_type = NXTRestConnection.get_image_content_type_by_filename(filename)
        header = {'Accept': image_header.value}

        file = open(filename, "rb").read()

        return self.rest_connection.put('/camera/image/testimage/custom', content_type=content_type, data=file,
                                        additional_headers=header)

    def get_roi_options(self):
        return self.rest_connection.options('/camera/roi').to_json()

    def get_camera_roi(self) -> CameraRoi:
        return CameraRoi.from_json(self.rest_connection.get("/camera/roi").to_json()).to_json()

    def set_camera_roi(self, camera_roi: CameraRoi):
        param = camera_roi.to_json()
        header = {'Accept': '*/*'}
        return self.rest_connection.patch('/camera/roi',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationXWwwFormUrlencoded,
                                          params=param, additional_headers=header)

    def get_trigger_options(self):
        return self.rest_connection.options('/camera/trigger').to_json()

    # def get_trigger(self):
    #     return self.rest_connection.get('/camera/trigger', content_type=NxtRestConnection.HttpContentTypes.
    #                                     ApplicationJson).to_json()

    def set_camera_trigger_type(self, trigger_type: TriggerSettingsBase.TRIGGERTYPE):
        params = {'TriggerType': trigger_type.value}
        return self.rest_connection.patch("/camera/trigger", params=params)

    def set_camera_trigger_to_software(self):
        params = {'TriggerType': 'Software'}
        return self.rest_connection.patch("/camera/trigger", params=params)

    def get_trigger_settings(self) -> TriggerSettingsBase:
        """Returns the trigger settings like Edge, TriggerType etc. in form of a TriggerSetting Object"""
        return self.trigger_setting_class.from_json(self.rest_connection.get('/camera/trigger',
                                                                             content_type=NXTRestConnection.
                                                                             HttpContentTypes.ApplicationJson).
                                                    to_json())

    def trigger(self):
        """Generates a software trigger. Trigger mode must be set to software,
        otherwise this command will not have any effects."""
        return self.rest_connection.post("/camera/trigger")
