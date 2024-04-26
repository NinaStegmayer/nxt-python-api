import json
import time
from nxt_vapp_handler import NXTVAppHandler
from nxt_rest_connection import NXTRestConnection
from utils.dto.roi_config import RoiConfig
from utils.dto.object_detector_result import ObjectDetectorResult
from utils.dto.roi_object import RoiObject
from errors.vision_app_error import ResultImageNotFound


class NXTVAppObjectDetector:
    """Specialized NXTVAppHandler class for the Object Detector Vision App.

    Provides functions to set / get ROIs and Configurables (such as current CNNs, detection threshold).
    Enables to install / delete CNNs and returns results

    Requires an established NxtRestConnection.

    Note: get_result_image only available from v.4"""

    def __init__(self, rest_connection: NXTRestConnection):
        self.vapp = "objectdetector"
        self.vapp_handler = NXTVAppHandler(rest_connection, self.vapp)

    # ROI
    def set_roi(self, roi: RoiObject):
        roi_name = roi.to_json()["Identifier"]
        return self.vapp_handler.set_single_roi_position(roi_name, roi)

    def get_current_roiconfig(self) -> json:
        return self.vapp_handler.get_roi_config()

    def gets_single_roi_position(self, roi_name: str) -> RoiObject:
        return self.vapp_handler.get_single_roi_position(roi_name)

    def set_roiconfig(self, new_roi_config: RoiConfig):
        self.vapp_handler.set_roi_config(new_roi_config)

    def delete_single_roi(self, roi_name: str, roi_config: RoiConfig):
        self.vapp_handler.delete_single_roi(roi_name, roi_config)

    def delete_all_rois(self, roi_config: RoiConfig):
        self.vapp_handler.delete_all_rois(roi_config)

    # CONFIGURABLES
    def get_available_cnns(self):
        return self.vapp_handler.configurable_int_double_string_enum_range("a_cnns")

    def get_current_cnn(self) -> str:
        return self.vapp_handler.configurable_int_double_string_enum_get("a_cnns")

    def set_current_cnn(self, cnn: str):
        return self.vapp_handler.configurable_int_double_string_enum_set("a_cnns", cnn)

    def set_threshold(self, value: int):
        self.vapp_handler.configurable_int_double_string_enum_set("detectionthreshold", value)

    def get_threshold(self) -> int:
        return self.vapp_handler.configurable_int_double_string_enum_get("detectionthreshold")

    def show_result_image(self, value: bool):
        self.vapp_handler.configurable_int_double_string_enum_set("vapp_result_image", value)

    def save_result_image(self, file_name: str):
        if self.vapp_handler.configurable_int_double_string_enum_get("vapp_result_image") is True:
            i = 0
            while i < 10:
                try:
                    self.vapp_handler.save_custom_result_image("default", file_name)
                    break
                except:
                    pass
                time.sleep(0.5)
                i += 1
            print("Wait some time until resultimage is available.")
        else:
            raise ResultImageNotFound("vapp_result_image")

    # FILES
    def install_cnn(self, cnn_file: str):
        available_cnns = self.get_available_cnns()
        self.vapp_handler.configurable_file_upload("cnnfile", cnn_file)

        while True:
            if available_cnns != self.get_available_cnns():
                break
            print("Cnn installing. Wait some time")
            time.sleep(0.5)

    def delete_active_cnn(self):
        available_cnns = self.get_available_cnns()

        if 'NoCNNInstalled' in available_cnns:
            print("Can not delete active CNN: No CNN installed")
            return

        self.vapp_handler.configurable_file_delete("cnnfile")

        while True:
            if available_cnns != self.get_available_cnns():
                break
            print("Wait till CNN is deleted")
            time.sleep(0.5)

    # RESULTS
    def get_last_detection_resultsources(self) -> ObjectDetectorResult:
        result = self.vapp_handler.get_resultsource_last()

        return ObjectDetectorResult(result["count"], result["data"], result["detection"], result["highlight"])

    def get_result_highlight(self):
        resultsource = self.vapp_handler.get_resultsource_last()
        return resultsource["count"]

    # WEBSITE
    def get_website(self):
        return self.vapp_handler.get_website()
