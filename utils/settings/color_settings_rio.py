import json
from enum import Enum

from utils.settings.color_settings_base import ColorSettingsBase


class ColorSettingsRio(ColorSettingsBase):
    """
            Class to manage all attributes concerning the color settings needed in the NxtCameraHandler.

            Inherits from ColorSettingsBase.

           Enables code completion and to only set/get valid and available settings
           (BlueGain, GreenGain, RedGain, WhiteBalance).

           Contains Enum for the WhiteBalance setting [OFF, CONTINUOUS, ONCE].

           NOTE: only available on color sensors!"""
    class WHITEBALANCE(Enum):
        OFF = "Off"
        CONTINUOUS = "Continuous"
        ONCE = "Once"

    def __init__(self):
        super().__init__()

    def from_json(self, data: json):
        self.BlueGain = data["BlueGain"]
        self.GreenGain = data["GreenGain"]
        self.RedGain = data["RedGain"]
        self.WhiteBalance = self.WHITEBALANCE(data["WhiteBalance"])
        return self
