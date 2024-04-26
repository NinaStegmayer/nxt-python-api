import json
from enum import Enum
from config.nxt_config import NXTConfig
from nxt_rest_connection import NXTRestConnection


class NXTGPIOHandlerMalibu:
    """Provides functions to address the GPIO node of an IDS NXT malibu Camera.
        Requires an established NxtRestConnection."""
    def __init__(self, rest_connection: NXTRestConnection):
        self.rest_connection = rest_connection

    def get_gpio_pins(self) -> list[str]:
        """Lists all available gpio pins"""
        return self.rest_connection.options('/gpio').to_json()["Objects"]

    def get_gpio_pin_options(self, pin: str) -> json:
        """Lists all options of the specified pin such as descriptions and ranges of the available attributes."""
        return self.rest_connection.options(f'/gpio/{pin}').to_json()

    def get_gpio_pin(self, pin: str) -> json:
        """Returns the status information of the selected pin like e.g. level."""
        return self.rest_connection.get(f'/gpio/{pin}').to_json()

    class Mode(Enum):
        """Required to set GPIO Pin Mode"""
        INPUT = "Input"
        OUTPUT = "Output"

    def set_gpio_pin(self, pin: str, inverter: bool, level: bool, mode: Mode):
        """Inverter(bool): Enabled additional inverter. If 'true', 0 V input means on-level.

        Level(bool): Logic-Level, note that true hardware level depends on invert. This can only be set if the GPIO mode is configured as output.

        Mode(Mode(Enum)): Pin title (In-/Output)"""
        header = {'Accept': '*/*'}
        params = {'Inverter': inverter, 'Level': level, 'Mode': mode.value}
        self.rest_connection.patch(f'/gpio/{pin}', NXTRestConnection.HttpContentTypes.ApplicationXWwwFormUrlencoded,
                                   additional_headers=header, params=params)


if __name__ == "__main__":
    config = NXTConfig()
    nxt_rest = NXTRestConnection(config.ip, config.user, config.password)
    gpio_handler = NXTGPIOHandlerMalibu(nxt_rest)
    print(gpio_handler.get_gpio_pins())
    print(gpio_handler.get_gpio_pin("pin1"))
    gpio_handler.set_gpio_pin("pin1", False, True, gpio_handler.Mode.OUTPUT)
    print(gpio_handler.get_gpio_pin("pin1"))
