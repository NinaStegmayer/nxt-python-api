import json
from enum import Enum


class ColorSettingsBase:
    """
        Class to manage all attributes concerning the color settings needed in the NxtCameraHandler.

        Is inherited from ColorSettingsRio and ColorSettingsMalibu.

        Contains Enum for the WhiteBalance setting.

        NOTE: only available on color sensors!"""
    class WHITEBALANCE(Enum):
        OFF = "Off"
        CONTINUOUS = "Continuous"

    def __init__(self):

        self.BlueGain: float = None
        self.GreenGain: float = None
        self.RedGain: float = None
        self.WhiteBalance: ColorSettingsBase.WHITEBALANCE = None

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
        """implemented by the inheriting classes such as ColorSettingsRio and ColorSettingsMalibu"""
        pass


