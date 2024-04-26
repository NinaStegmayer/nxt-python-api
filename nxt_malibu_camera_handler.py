from nxt_camera_handler_base import NXTCameraHandlerBase
from nxt_rest_connection import NXTRestConnection
from utils.settings.camera_settings_malibu import CameraSettingsMalibu
from utils.settings.color_settings_malibu import ColorSettingsMalibu
from utils.settings.trigger_settings_malibu import TriggerSettingsMalibu


class NXTMalibuCameraHandler(NXTCameraHandlerBase):
    """
        Provides functions to set / get camera, color , trigger, roi settings for IDS NXT malibu .

        Inherits from NxtCameraHandler.

        Requires an established NxtRestConnection.

        Note: color settings only available on color sensors  """

    def __init__(self, rest_connection: NXTRestConnection):
        super().__init__(rest_connection)
        self.camera_setting_class = CameraSettingsMalibu()
        self.color_setting_class = ColorSettingsMalibu()
        self.trigger_setting_class = TriggerSettingsMalibu()

    def get_camera_settings(self) -> CameraSettingsMalibu:
        """Returns the camera settings like exposure time, gain etc. as camera specific CameraSettings Object"""
        return self.camera_setting_class.from_json(self.rest_connection.get('/camera',
                                                                            content_type=NXTRestConnection.
                                                                            HttpContentTypes.ApplicationJson).to_json())

    def set_camera_settings_class(self, settings: CameraSettingsMalibu):
        """Changes the camera setting. Requires a new initialised CameraSettingsMalibu object.
                                Do not use the class intern camera_settings object as parameter!"""
        settings_dict = {}
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
        if settings.BrightnessAuto is not None:
            settings_dict["BrightnessAuto"] = settings.BrightnessAuto
        if settings.BrightnessAutoThreshold is not None:
            settings_dict["BrightnessAutoThreshold"] = settings.BrightnessAutoThreshold
        if settings.Contrast is not None:
            settings_dict["Contrast"] = settings.Contrast
        if settings.MCTF is not None:
            settings_dict["MCTF"] = settings.MCTF
        if settings.SharpeningStrength is not None:
            settings_dict["SharpeningStrength"] = settings.SharpeningStrength
        if settings.NightMode is not None:
            settings_dict["NightMode"] = settings.NightMode

        return self.rest_connection.patch('/camera',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=settings_dict)

    def set_color_settings(self, color_settings: ColorSettingsMalibu):
        """Changes the color setting. Requires a new initialised ColorSettingsMalibu object.
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
        if color_settings.ColorBrightness is not None:
            color_settings_dict["ColorBrightness"] = color_settings.ColorBrightness
        if color_settings.ColorHue is not None:
            color_settings_dict["ColorHue"] = color_settings.ColorHue
        if color_settings.ColorSaturation is not None:
            color_settings_dict["ColorSaturation"] = color_settings.ColorSaturation

        return self.rest_connection.patch('/camera/color',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=color_settings_dict)

    def set_trigger_settings(self, trigger_settings: TriggerSettingsMalibu):
        """Changes the trigger setting. Requires a new initialised TriggerSettingsMalibu object.
        Do not use the class intern trigger_settings object as parameter!"""
        trigger_settings_dict = {}
        if trigger_settings.Edge is not None:
            trigger_settings_dict["Edge"] = trigger_settings.Edge.value
        if trigger_settings.NoTriggerThreshold_ms is not None:
            trigger_settings_dict["NoTriggerThreshold"] = trigger_settings.NoTriggerThreshold_ms
        if trigger_settings.TriggerType is not None:
            trigger_settings_dict["TriggerType"] = trigger_settings.TriggerType.value

        return self.rest_connection.patch('/camera/trigger',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=trigger_settings_dict)

