import json
from enum import Enum

from utils.settings.camera_settings_base import CameraSettingsBase


class CameraSettingsRio(CameraSettingsBase):
    """
            Class to manage all attributes concerning the IDS NXT rio camera settings needed in the NxtCameraHandler.

            Inherits from CameraSettingsBase.

           Enables code completion and to only set/get valid and available settings
           (Binning, ExposureTime, FlipHorizontal, FlipVertical, Gain, GainAuto, GammaCorrection,
           LineRate, LineScanMode, LineTrigger).

           Contains Enums for the Binning and GainAuto settings.

           NOTE: LineRate can only be set if LineScanMode is enabled.
           LineScanMode and Binning can not be set simultaneously.
    """

    class BINNING(Enum):
        OFF = "Off"
        TWOxTWO = "2x2"
        FOURxFOUR = "4x4"

    class GAINAUTO(Enum):
        OFF = "Off"
        CONTINUOUS = "Continuous"
        ONCE = "Once"

    def __init__(self):
        super().__init__()
        self.Binning: CameraSettingsRio.BINNING = None
        self.GammaCorrection: float = None
        self.LineRate: int = None
        self.LineScanMode: bool = None
        self.LineTrigger: bool = None

    def from_json(self, data: json):
        self.Binning = self.BINNING(data["Binning"])
        self.ExposureTime = data["ExposureTime"]
        self.FlipHorizontal = data["FlipHorizontal"]
        self.FlipVertical = data["FlipVertical"]
        self.Gain = data["Gain"]
        self.GainAuto = self.GAINAUTO(data["GainAuto"])
        self.GammaCorrection = data["GammaCorrection"]
        self.LineRate = data["LineRate"]
        self.LineScanMode = data["LineScanMode"]
        self.LineTrigger = data["LineTrigger"]
        return self
