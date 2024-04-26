import json
import os
import time

from logs.logger import nxt_logger
from utils.dto.roi_object import RoiObject
from utils.dto.roi_config import RoiConfig
from utils.dto.rest_result import RestResult
from nxt_rest_connection import NXTRestConnection


class NXTVAppHandler:
    """Basis class to communicate with VisionApps via given established REST connection.
    e.g. install / (de)activate / delete Vision App

        Implements basic functions used by the specialised VisionApps to manage configuration of ROIs,
        app specific configurables, file handling (upload, download, delete...) """

    def __init__(self, rest_connection: NXTRestConnection, vapp: str):
        self.rest_connection = rest_connection
        self.vapp = vapp

    def setup_vapp(self, vapp_path: str, vapp_name: str):
        """Deactivates running Vision Apps then installs and activates given Vision App """
        if vapp_name not in self.get_vapps_running():
            self.deactivate_running_vapps()
            while True:
                if not self.get_vapps_running():
                    break
                nxt_logger.info("Deactivating running Vapps. Wait some time")
                time.sleep(0.5)
            self.install_vapp(vapp_path, vapp_name)
            while True:
                if vapp_name in self.get_vapps_installed():
                    break
                nxt_logger.info("Installing VApp. Wait some time")
                time.sleep(0.5)
            self.activate_vapp(vapp_name)
            while True:
                if vapp_name in self.get_vapps_running():
                    break
                nxt_logger.info("Activating VApp. Wait some time")
                time.sleep(0.5)

    def get_vapp(self) -> str:
        """Returns name of the Vision App."""
        return self.vapp

    def get_vapp_version(self, vapp: str):
        return self.rest_connection.get(f'/vapps/{vapp}').to_json()["Version"]

    def get_vapps_installed(self) -> [str]:
        vapp_object = self.rest_connection.get(f'/vapps/').to_json()
        return vapp_object["Installed"]

    def get_vapps_running(self) -> [str]:
        running_vapps = []
        installed_vapps = self.get_vapps_installed()

        for vapp in installed_vapps:
            vapp_status = self.rest_connection.get(f'/vapps/{vapp}').to_json()["Status"]
            if vapp_status == "Running":
                running_vapps.append(vapp)

        return running_vapps

    def install_vapp(self, filepath: str, vapp: str):
        header = {'Accept': '*/*'}
        content_type = NXTRestConnection.HttpContentTypes.ApplicationVapp
        with open(filepath, 'rb') as data:
            self.rest_connection.put(f'/vapps/{vapp}', content_type=content_type, additional_headers=header,
                                     data=data.read())

    def activate_vapp(self, vapp: str):
        header = {'Accept': '*/*'}
        self.rest_connection.put(f'/vapps/activated/{vapp}', additional_headers=header)

    def deactivate_vapp(self, vapp: str):
        header = {'Accept': '*/*'}
        self.rest_connection.delete(f'/vapps/activated/{vapp}', additional_headers=header)

    def deactivate_running_vapps(self):
        for app in self.get_vapps_running():
            self.deactivate_vapp(app)

    def delete_vapp(self, vapp: str):
        header = {'Accept': '*/*'}
        content_type = NXTRestConnection.HttpContentTypes.ApplicationVapp
        self.rest_connection.delete(f'/vapps/{vapp}', content_type=content_type, additional_headers=header)

    def get_single_rois(self) -> list[str]:
        options_json = self.rest_connection.options(f'/vapps/{self.vapp}/rois').to_json()

        return options_json["Objects"]

    def set_single_roi_position(self, roi_name: str, new_roi: RoiObject):
        params = new_roi.to_json()
        del params["Identifier"]
        self.rest_connection.patch(f'/vapps/{self.vapp}/rois/{roi_name}', params=params)

    def get_single_roi_position(self, roi_name: str) -> RoiObject:
        roi = RoiObject.from_json(
            self.rest_connection.get(f'/vapps/{self.vapp}/rois/{roi_name}').to_json())
        roi.identifier = roi_name
        return roi

    def get_roi_config(self) -> json:
        return self.rest_connection.get(f'/vapps/{self.vapp}/roimanager/roiconfig',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson)

    def set_roi_config(self, new_roi_config: RoiConfig):
        """PUTs the ROI configuration on the vision app."""
        roi_json_string_data = json.dumps(new_roi_config.to_map()).encode('utf-8')
        self.rest_connection.put(f'/vapps/{self.vapp}/roimanager/roiconfig', data=roi_json_string_data,
                                 content_type=NXTRestConnection.HttpContentTypes.ApplicationJson)

    def delete_single_roi(self, roi_name: str, roi_config: RoiConfig):
        """DELETEs a single ROI from the vision app and the RoiConfig Object."""
        self.rest_connection.delete(f'/vapps/{self.vapp}/rois/{roi_name}')
        roi_config.delete_roi(roi_config.get_roi(roi_name))

    def delete_all_rois(self, roiconfig: RoiConfig):
        """DELETEs all ROIs from the vision app and the RoiConfig Object."""
        self.rest_connection.delete(f'/vapps/{self.vapp}/rois')
        roiconfig.roi_config = []

    def get_resultsource_last(self) -> json:
        """Returns the data of the last result source"""
        this_result = self.rest_connection.get(f'/vapps/{self.vapp}/resultsources/last')
        return this_result.to_json()

    def get_configurables(self) -> json:
        """Returns the configurables of the vision app."""
        return self.rest_connection.get(f'/vapps/{self.vapp}/configurables').to_json()

    def configurable_int_double_string_enum_get(self, configurable_name: str) -> int | float | str | bool:
        """Returns the specified configurable of the vision app."""
        return self.rest_connection.get(f'/vapps/{self.vapp}/configurables').to_json()[configurable_name]

    def configurable_int_double_string_enum_set(self, configurable_name: str,
                                                value: int | float | str | bool) -> RestResult:
        """Changes the specified configurable of the vision app."""
        param = {configurable_name: value}

        return self.rest_connection.patch(f'/vapps/{self.vapp}/configurables',
                                          NXTRestConnection.HttpContentTypes.ApplicationXWwwFormUrlencoded,
                                          param)

    def configurable_int_double_string_enum_range(self, configurable_name: str):
        """Lists the ranges of the specified configurable."""
        options_json = self.rest_connection.options(f'/vapps/{self.vapp}/configurables').to_json()
        return options_json['GET']["application/json"]["Values"][configurable_name]["Range"]

    def configurable_file_upload(self, configurable_file_name: str, file: str) -> RestResult:
        """Sets the selected file."""
        with open(file, 'rb') as file_data:
            filename = os.path.basename(file)
            additional_param = {'Content-Disposition': f'attachment; filename={filename}'}

            return self.rest_connection.put(
                f'/vapps/{self.vapp}/files/{configurable_file_name}/data',
                NXTRestConnection.HttpContentTypes.ApplicationOctetStream,
                additional_headers=additional_param, data=file_data.read())

    def configurable_file_download(self, configurable_file_name: str) -> RestResult:
        """Returns the data of the selected file."""
        return self.rest_connection.get(
            f'/vapps/{self.vapp}/files/{configurable_file_name}/data')

    def configurable_file_delete(self, configurable_file_name: str) -> RestResult:
        """Deletes the selected file."""
        return self.rest_connection.delete(
            f'/vapps/{self.vapp}/files/{configurable_file_name}/data',
            NXTRestConnection.HttpContentTypes.ApplicationOctetStream)

    def save_custom_result_image(self, image_name: str, file_name: str):
        """saves the specified image ("attentionmap" / "anomalymap" / "default" for result image) under the specified
        file name (.jpg format by default)"""

        try:
            if isinstance(NXTRestConnection.get_image_accept_header_by_filename(file_name),
                          NXTRestConnection.HttpAccept):
                image_format = NXTRestConnection.get_image_accept_header_by_filename(file_name)
        except:
            image_format = NXTRestConnection.HttpAccept.ImageJpeg
            file_name += ".jpeg"

        image_header = {'Accept': image_format.value}
        params = {'quality': 80}

        with open(file_name, 'wb') as file:
            file.write(self.rest_connection.get(f'/vapps/{self.vapp}/images/{image_name}',
                                                            params=params,
                                                            additional_headers=image_header).response_data)

    def get_website(self) -> RestResult:
        """Returns the website of the selected vision app.
        The website of a vision app can be opened via http://<camera IP address>/vapps/<vision app>/website."""

        return self.rest_connection.get(f'/vapps/{self.vapp}/website')
