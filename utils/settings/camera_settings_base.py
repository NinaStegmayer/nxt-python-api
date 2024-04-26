import json
from enum import Enum


class CameraSettingsBase:
    """
                Base Class to manage all attributes concerning the camera settings needed in the NxtCameraHandler.

                Is inherited from CameraSettingsRio and CameraSettingsMalibu.

        """
    class GAINAUTO(Enum):
        """specified by the inheriting classes such as CameraSettingsRio and CameraSettingsMalibu"""
        pass

    def __init__(self):
        self.ExposureTime: int = None
        self.FlipHorizontal: bool = None
        self.FlipVertical: bool = None
        self.Gain: int = None
        self.GainAuto: CameraSettingsBase.GAINAUTO = None

    def to_json(self):
        json_dict = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    json_dict[attr] = value.value
                else:
                    json_dict[attr] = value
        return json_dict

    def from_json(self, data: json):
        """implemented by the inheriting classes such as CameraSettingsRio and CameraSettingsMalibu"""
        pass
