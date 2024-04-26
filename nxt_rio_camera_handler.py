from nxt_camera_handler_base import NXTCameraHandlerBase
from nxt_rest_connection import NXTRestConnection
from utils.settings.camera_settings_rio import CameraSettingsRio
from utils.settings.color_settings_rio import ColorSettingsRio
from utils.settings.trigger_settings_rio import TriggerSettingsRio


class NXTRioCameraHandler(NXTCameraHandlerBase):
    """
        Provides functions to set / get camera, color , trigger, roi settings for IDS NXT rio .

        Inherits from NxtCameraHandler.

        Enables linescan to be (de)activated.

        Requires an established NxtRestConnection.

        Note: color settings only available on color sensors"""

    def __init__(self, rest_connection: NXTRestConnection):
        super().__init__(rest_connection)
        self.camera_setting_class = CameraSettingsRio()
        self.color_setting_class = ColorSettingsRio()
        self.trigger_setting_class = TriggerSettingsRio()

    def get_camera_settings(self) -> CameraSettingsRio:
        """Returns the camera settings like exposure time, gain etc. as camera specific CameraSettings Object"""
        return self.camera_setting_class.from_json(self.rest_connection.get('/camera',
                                                                            content_type=NXTRestConnection.
                                                                            HttpContentTypes.ApplicationJson).to_json())

    def set_camera_settings_class(self, settings: CameraSettingsRio):
        """Changes the camera setting. Requires a new initialised CameraSettingsRio object.
                                        Do not use the class intern camera_settings object as parameter!"""
        settings_dict = {}
        if settings.Binning is not None:
            settings_dict["Binning"] = settings.Binning.value
        if settings.ExposureTime is not None:
            settings_dict["ExposureTime"] = settings.ExposureTime
        if settings.FlipHorizontal is not None:
            settings_dict["FlipHorizontal"] = settings.FlipHorizontal
        if settings.FlipVertical is not None:
            settings_dict["FlipVertical"] = settings.FlipVertical
        if settings.Gain is not None:
            settings_dict["Gain"] = settings.Gain
        if settings.GainAuto is not None:
            settings_dict["GainAuto"] = settings.GainAuto.value
        if settings.GammaCorrection is not None:
            settings_dict["GammaCorrection"] = settings.GammaCorrection
        if settings.LineRate is not None:
            settings_dict["LineRate"] = settings.LineRate
        if settings.LineScanMode is not None:
            settings_dict["LineScanMode"] = settings.LineScanMode
        if settings.LineTrigger is not None:
            settings_dict["LineTrigger"] = settings.LineTrigger

        return self.rest_connection.patch('/camera',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=settings_dict)

    def enable_linescanmode(self, linescanmode: bool):
        param = {"LineScanMode": linescanmode}
        return self.rest_connection.patch('/camera', content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=param)

    def set_linerate(self, linerate: int):
        param = {"LineRate": linerate}
        return self.rest_connection.patch('/camera', content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=param)

    def set_color_settings(self, color_settings: ColorSettingsRio):
        """Changes the color setting. Requires a new initialised ColorSettingsRio object.
                        Do not use the class intern color_settings object as parameter!"""
        color_settings_dict = {}
        if color_settings.BlueGain is not None:
            color_settings_dict["BlueGain"] = color_settings.BlueGain
        if color_settings.GreenGain is not None:
            color_settings_dict["GreenGain"] = color_settings.GreenGain
        if color_settings.RedGain is not None:
            color_settings_dict["RedGain"] = color_settings.RedGain
        if color_settings.WhiteBalance is not None:
            color_settings_dict["WhiteBalance"] = color_settings.WhiteBalance.value

        return self.rest_connection.patch('/camera/color',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=color_settings_dict)

    def set_trigger_settings(self, trigger_settings: TriggerSettingsRio):
        """Changes the trigger setting. Requires a new initialised TriggerSettingsRio object.
                Do not use the class intern trigger_settings object as parameter!"""
        trigger_settings_dict = {}
        if trigger_settings.Debounce_us is not None:
            trigger_settings_dict["Debounce"] = trigger_settings.Debounce_us
        if trigger_settings.Delay_us is not None:
            trigger_settings_dict["Delay"] = trigger_settings.Delay_us
        if trigger_settings.Edge is not None:
            trigger_settings_dict["Edge"] = trigger_settings.Edge.value
        if trigger_settings.NoTriggerThreshold_ms is not None:
            trigger_settings_dict["NoTriggerThreshold"] = trigger_settings.NoTriggerThreshold_ms
        if trigger_settings.Prescaler is not None:
            trigger_settings_dict["Prescaler"] = trigger_settings.Prescaler
        if trigger_settings.Timeout_ms is not None:
            trigger_settings_dict["Timeout"] = trigger_settings.Timeout_ms
        if trigger_settings.TriggerType is not None:
            trigger_settings_dict["TriggerType"] = trigger_settings.TriggerType.value

        return self.rest_connection.patch('/camera/trigger',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=trigger_settings_dict)
