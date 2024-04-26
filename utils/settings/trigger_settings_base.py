import json
from enum import Enum


class TriggerSettingsBase:
    """
        Base class to manage all attributes concerning the trigger settings needed in the NxtCameraHandler.

        Is inherited from TriggerSettingsRio and TriggerSettingsMalibu.
    """
    class EDGE(Enum):
        RISING = "Rising"
        FALLING = "Falling"
        BOTH = "Both"

    class TRIGGERTYPE(Enum):
        FREERUN = "Freerun"
        SOFTWARE = "Software"
        HARDWARE = "Hardware"

    def __init__(self):
        self.Edge: TriggerSettingsBase.EDGE = None
        self.NoTriggerThreshold_ms: int = None
        """0 - 2147483647 in milliseconds. Maximum time between two received images before system state warning.  
        **NOTICE!** 0 deactivates the warning."""
        self.TriggerType: TriggerSettingsBase.TRIGGERTYPE = None

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
        """implemented by the inheriting classes such as TriggerSettingsRio and TriggerSettingsMalibu"""
        pass
