from config.nxt_config import NXTConfig
from nxt_rio_camera_handler import NXTRioCameraHandler
from nxt_rest_connection import NXTRestConnection

# How to set camera settings on an IDS NXT rio (equal to IDS NXT malibu except the creation of the CameraHandler
# -> needs to be a NXTMalibuCameraHandler)

if __name__ == "__main__":
    # generates new configuration of parameters defined in the config/config.ini
    config = NXTConfig()

    # establishes RestConnection with parameters defined in /config/config.ini
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    # creates an object of the Vision App
    camera_handler = NXTRioCameraHandler(rest_connection)

    # hovering over the method signature informs about the available settings that can be used to parametrize the method
    print(camera_handler.get_camera_settings_ranges(["ExposureTime", "Gain"]))

    # by calling the options method, a list informs about all options of the /camera node
    print(camera_handler.get_camera_settings_options())

    # verify if all settings are as required
    print(camera_handler.get_camera_settings().to_json())

    # one setting can easily be modified by executing the following method
    camera_handler.set_camera_setting("FlipVertical", True)

    # informs about the /camera/color node
    print(camera_handler.get_color_settings_options())

    camera_handler.set_color_setting("BlueGain", 70)

    print(camera_handler.get_color_settings().to_json())
