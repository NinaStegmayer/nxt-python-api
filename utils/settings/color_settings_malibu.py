import json

from utils.settings.color_settings_base import ColorSettingsBase


class ColorSettingsMalibu(ColorSettingsBase):
    """
                Class to manage all attributes concerning the color settings needed in the NxtCameraHandler.

                Inherits from ColorSettingsBase.

               Enables code completion and to only set/get valid and available settings
               (BlueGain, GreenGain, RedGain, WhiteBalance, ColorBrightness, ColorHue, ColorSaturation).

               Contains Enum for the WhiteBalance setting [OFF, CONTINUOUS].

               NOTE: only available on color sensors!"""

    def __init__(self):
        super().__init__()
        self.ColorBrightness: int = None
        self.ColorHue: int = None
        self.ColorSaturation: int = None

    def from_json(self, data: json):
        self.BlueGain = data["BlueGain"]
        self.GreenGain = data["GreenGain"]
        self.RedGain = data["RedGain"]
        self.WhiteBalance = self.WHITEBALANCE(data["WhiteBalance"])
        self.ColorBrightness = data["ColorBrightness"]
        self.ColorHue = data["ColorHue"]
        self.ColorSaturation = data["ColorSaturation"]
        return self
