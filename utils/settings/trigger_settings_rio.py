import json
from utils.settings.trigger_settings_base import TriggerSettingsBase


class TriggerSettingsRio(TriggerSettingsBase):
    """Class to manage all attributes concerning the trigger settings needed in the NxtCameraHandler.

    Enables code completion and to only set/get valid and available settings
    (Debounce, Delay, Edge, NoTriggerThreshold, Prescaler, Timeout, TriggerType).

    Contains Enums for the edge and the trigger type settings. """

    def __init__(self):
        super().__init__()
        self.Debounce_us: int = None
        """0 - 20971 in microseconds"""
        self.Delay_us: int = None
        """ 0 - 16777215 in microseconds"""
        self.Prescaler: int = None
        """1 - 64"""
        self.Timeout_ms: int = None
        """0 - 16777215 in microseconds"""

    def from_json(self, data: json):
        self.Debounce_us = data["Debounce"]
        self.Delay_us = data["Delay"]
        self.Edge = TriggerSettingsRio.EDGE(data["Edge"])
        self.NoTriggerThreshold_ms = data["NoTriggerThreshold"]
        self.Prescaler = data["Prescaler"]
        self.Timeout_ms = data["Timeout"]
        self.TriggerType = TriggerSettingsRio.TRIGGERTYPE(data["TriggerType"])
        return self
