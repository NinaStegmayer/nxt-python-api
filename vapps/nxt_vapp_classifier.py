import json

from nxt_vapp_handler import NXTVAppHandler
from logs.logger import nxt_logger
from nxt_rest_connection import NXTRestConnection
from utils.dto.roi_config import RoiConfig
import time
from utils.dto.roi_object import RoiObject
from errors.vision_app_error import ResultImageNotFound, AttentionMapNotAvailable


class NXTVAppClassifier:
    """Specialized NXTVAppHandler class for the Classifier Vision App.

        Provides functions to set / get ROIs and Configurables (such as current CNNs, availability of the attentionmap).
        Enables to install / delete CNNs and returns results.

        Requires an established NxtRestConnection.
    """

    def __init__(self, rest_connection: NXTRestConnection):
        self.vapp = "classifier"
        self.vapp_handler = NXTVAppHandler(rest_connection, self.vapp)

    # ROI
    def set_roi(self, roi: RoiObject):
        roi_name = roi.to_json()["Identifier"]
        return self.vapp_handler.set_single_roi_position(roi_name, roi)

    def gets_single_roi_position(self, roi_name: str):
        return self.vapp_handler.get_single_roi_position(roi_name)

    def get_current_roi_config(self) -> json:
        return self.vapp_handler.get_roi_config()

    def set_roiconfig(self, new_roi_config: RoiConfig):
        self.vapp_handler.set_roi_config(new_roi_config)

    def delete_single_roi(self, roi_name: str, roi_config: RoiConfig):
        self.vapp_handler.delete_single_roi(roi_name, roi_config)

    def delete_all_rois(self, roi_config: RoiConfig):
        self.vapp_handler.delete_all_rois(roi_config)

    # CONFIGURABLES
    def get_available_cnns(self) -> [str]:
        return self.vapp_handler.configurable_int_double_string_enum_range("cnn")

    def get_current_cnn(self) -> str:
        return self.vapp_handler.configurable_int_double_string_enum_get("cnn")

    def set_current_cnn(self, cnn: str):
        return self.vapp_handler.configurable_int_double_string_enum_set("cnn", cnn)

    def show_attention_map(self, value: bool):
        if "enable_attentionmap" in self.vapp_handler.get_configurables():
            self.vapp_handler.configurable_int_double_string_enum_set("enable_attentionmap", value)
        else:
            raise AttentionMapNotAvailable

    def save_result_image(self, file_name: str):
        self.vapp_handler.save_custom_result_image("default", file_name)

    def save_attention_map(self, file_name: str):
        if "enable_attentionmap" in self.vapp_handler.get_configurables():
            if self.vapp_handler.configurable_int_double_string_enum_get("enable_attentionmap") is True:
                i = 0
                while i < 10:
                    try:
                        self.vapp_handler.save_custom_result_image("attentionmap", file_name)
                        break
                    except:
                        pass
                    time.sleep(0.5)
                    i += 1
            else:
                raise ResultImageNotFound("enable_attentionmap")
        else:
            raise AttentionMapNotAvailable

    # FILES
    def install_cnn(self, cnn_file: str):
        available_cnns = self.get_available_cnns()
        self.vapp_handler.configurable_file_upload("cnnfile", cnn_file)

        while True:
            if available_cnns != self.get_available_cnns():
                break
            nxt_logger.info("Cnn installing. Wait some time")
            time.sleep(0.5)

    def delete_active_cnn(self):
        available_cnns = self.get_available_cnns()

        if 'NoCNNInstalled' in available_cnns:
            nxt_logger.warn("Can not delete active CNN: No CNN installed")
            return

        self.vapp_handler.configurable_file_delete("cnnfile")

        while True:
            if available_cnns != self.get_available_cnns():
                break
            nxt_logger.info("Wait till CNN is deleted")
            time.sleep(0.5)

    # RESULTS
    def get_last_detection_resultsources(self) -> json:
        return self.vapp_handler.get_resultsource_last()

    #   WEBSITE
    def get_website(self):
        return self.vapp_handler.get_website()
