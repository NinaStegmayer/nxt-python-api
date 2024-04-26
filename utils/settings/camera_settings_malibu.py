import json
from enum import Enum
from utils.settings.camera_settings_base import CameraSettingsBase


class CameraSettingsMalibu(CameraSettingsBase):
    """
            Class to manage all attributes concerning the IDS NXT malibu camera settings needed in the NxtCameraHandler.

            Inherits from CameraSettingsBase.

            Enables code completion and to only set/get valid and available settings
            (BrightnessAuto, BrightnessAutoThreshold, Contrast, ExposureTime, FlipHorizontal, FlipVertical, Gain,
            GainAuto, MCTF, NightMode, SharpeningStrength).

            Contains Enums for the GainAuto setting.

     """

    class GAINAUTO(Enum):
        OFF = "Off"
        CONTINUOUS = "Continuous"

    def __init__(self):
        super().__init__()
        self.BrightnessAuto: bool = None
        self.BrightnessAutoThreshold: int = None
        self.Contrast: int = None
        self.MCTF: int = None
        self.SharpeningStrength: int = None
        self.NightMode: bool = None

    def from_json(self, data: json):
        self.ExposureTime = data["ExposureTime"]
        self.FlipHorizontal = data["FlipHorizontal"]
        self.FlipVertical = data["FlipVertical"]
        self.Gain = data["Gain"]
        self.GainAuto = self.GAINAUTO(data["GainAuto"])
        self.BrightnessAuto = data["BrightnessAuto"]
        self.BrightnessAutoThreshold = data["BrightnessAutoThreshold"]
        self.Contrast = data["Contrast"]
        self.MCTF = data["MCTF"]
        self.SharpeningStrength = data["SharpeningStrength"]
        self.NightMode = data["NightMode"]
        return self
