import json
from utils.settings.trigger_settings_base import TriggerSettingsBase


class TriggerSettingsMalibu(TriggerSettingsBase):
    """Class to manage all attributes concerning the trigger settings needed in the NxtCameraHandler.

        Inherits from TriggerSettingsBase.

        Enables code completion and to only set/get valid and available settings
        (Edge, NoTriggerThreshold, TriggerType).

        Contains Enums for the edge and the trigger type settings. """
    def __init__(self):
        super().__init__()

    def from_json(self, data: json):
        self.Edge = TriggerSettingsMalibu.EDGE(data["Edge"])
        self.NoTriggerThreshold_ms = data["NoTriggerThreshold"]
        self.TriggerType = TriggerSettingsMalibu.TRIGGERTYPE(data["TriggerType"])
        return self

