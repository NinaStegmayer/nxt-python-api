from config.nxt_config import NXTConfig
from nxt_gpio_handler_rio import NXTGPIOHandlerRio
from nxt_rest_connection import NXTRestConnection
from logs.logger import nxt_logger # this import allows to use the project logger

if __name__ == "__main__":
    # generates new configuration of parameters defined in the config/config.ini
    config = NXTConfig()

    # establishes RestConnection with parameters defined in /config/config.ini
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    # creates a GPIO Handler for IDS NXT rio (for IDS NXT malibu create NXTGPIOHandlerMalibu(rest_connection)
    gpio_handler = NXTGPIOHandlerRio(rest_connection)

    gpio_handler.set_input_pin("in1", False)
    nxt_logger.info(gpio_handler.get_input_pin_info("in1"))

    gpio_handler.set_output_pin("out1", False, True)
    nxt_logger.info(gpio_handler.get_output_pin_info("out1"))
