import time
from nxt_vapp_handler import NXTVAppHandler
from logs.logger import nxt_logger
from nxt_rest_connection import NXTRestConnection
from utils.dto.anomaly_result import AnomalyResult
from errors.vision_app_error import ResultImageNotFound


class NXTVAppAnomalyFinder:
    """Specialized NXTVAppHandler class for the Anomaly Finder Vision App.

        Provides functions to adjust configurables (such as current CNNs, threshold, anomaly overlay, anomaly map).
        Enables to install / delete CNNs and returns results.

        Requires an established NxtRestConnection.
    """

    def __init__(self, rest_connection: NXTRestConnection):
        self.vapp = "anomalyfinder"
        self.vapp_handler = NXTVAppHandler(rest_connection, self.vapp)

    def set_threshold(self, value: float):
        self.vapp_handler.configurable_int_double_string_enum_set("threshold", value)

    def get_threshold(self) -> float:
        return self.vapp_handler.configurable_int_double_string_enum_get("threshold")

    def get_available_cnns(self) -> [str]:
        return self.vapp_handler.configurable_int_double_string_enum_range("cnns")

    def get_current_cnn(self) -> str:
        return self.vapp_handler.configurable_int_double_string_enum_get("cnns")

    def set_current_cnn(self, cnn: str):
        return self.vapp_handler.configurable_int_double_string_enum_set("cnns", cnn)

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

    def show_anomaly_overlay(self, value: bool):
        return self.vapp_handler.configurable_int_double_string_enum_set("show_anomaly_overlay", value)

    def show_anomaly_map(self, value: bool):
        return self.vapp_handler.configurable_int_double_string_enum_set("show_anomalymap", value)

    def save_anomaly_map(self, file_name: str):
        if self.vapp_handler.configurable_int_double_string_enum_get("show_anomalymap") is True:
            i = 0
            while i < 10:
                try:
                    self.vapp_handler.save_custom_result_image("anomalymap", file_name)
                    break
                except:
                    nxt_logger.info("Image not ready")
                time.sleep(0.5)
                i += 1

        else:
            raise ResultImageNotFound("show_anomalymap")

    def save_result_image(self, file_name: str):
        self.vapp_handler.save_custom_result_image("default", file_name)

    def get_last_anomaly_result(self) -> AnomalyResult:
        result = self.vapp_handler.get_resultsource_last()
        return AnomalyResult(result["anomaly"], result["score"], result["inferencetime"])
