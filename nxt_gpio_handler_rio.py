from nxt_rest_connection import NXTRestConnection


class NXTGPIOHandlerRio:
    """Provides functions to address the GPIO node of an IDS NXT rio Camera.
    Requires an established NXTRestConnection."""

    def __init__(self, rest_connection: NXTRestConnection):
        self.rest_connection = rest_connection

    def get_gpio_node(self):
        """Lists all options of the /gpio node."""
        return self.rest_connection.options('/gpio')

    def get_all_input_pins(self):
        return self.rest_connection.options('/gpio/inputs')

    def get_input_pin_info(self, pin: str):
        return self.rest_connection.get(f'/gpio/inputs/{pin}')

    def set_input_pin(self, pin: str, inverter: bool):
        """Inverter: Enabled additional inverter. If 'true', 0 V input means on-level."""
        header = {'Accept': '*/*'}
        params = {'Inverter': inverter}
        self.rest_connection.patch(f'/gpio/inputs/{pin}', additional_headers=header, params=params)

    def get_all_output_pins(self):
        return self.rest_connection.options('/gpio/outputs')

    def get_output_pin_info(self, pin: str):
        return self.rest_connection.get(f'/gpio/outputs/{pin}')

    def set_output_pin(self, pin: str, inverter: bool, level: bool):
        """Inverter: Enabled additional inverter. If true, 0 V input means on-level.
        Level: Logic-Level, note that true hardware level depends on invert."""
        header = {'Accept': '*/*'}
        params = {'Inverter': inverter, 'Level': level}
        self.rest_connection.patch(f'/gpio/outputs/{pin}', additional_headers=header, params=params)
