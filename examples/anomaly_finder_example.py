# The following code is required for each example:
from config.nxt_config import NXTConfig
from logs.logger import nxt_logger  # this import allows to use the project logger
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_anomaly_finder import NXTVAppAnomalyFinder

if __name__ == "__main__":
    # generates new configuration of parameters defined in the config/config.ini
    config = NXTConfig()

    CNN_PATH = r"{absolute path from your directory to required CNN}"
    """requires absolute path to the CNN with file ending 
        .rano for IDS NXT rio Cameras / .mano for IDS NXT malibu Cameras"""

    CNN_NAME = 'your_cnn'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to anomaly finder vision app}"
    """requires absolute path of the Vision App with file ending .vapp"""

    # establishes RestConnection with parameters defined in /config/config.ini
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    # creates an object of the Vision App
    anomaly_finder_app = NXTVAppAnomalyFinder(rest_connection)

    # Deactivates running Vision Apps then installs and activates given Vision App
    anomaly_finder_app.vapp_handler.setup_vapp(VAPP_PATH, anomaly_finder_app.vapp)

# Example 1: configure the required CNN

    # display the CNNs already installed
    nxt_logger.info(anomaly_finder_app.get_available_cnns())

    # if the required CNN is not already installed you need to install it (*.rano if using an IDS NXT rio /
    # *.mano if IDS NXT malibu is used):
    anomaly_finder_app.install_cnn(CNN_PATH)  # specify the path of the CNN: keep in mind that it needs to be a valid name!

    # specify the required CNN:
    anomaly_finder_app.set_current_cnn(CNN_NAME)  # enter name of the CNN

    # delete the current CNN:
    anomaly_finder_app.delete_active_cnn()


# Example 2: configure the required threshold

    anomaly_finder_app.set_threshold(70)


# Example 3: display and log the latest results

    nxt_logger.info(anomaly_finder_app.get_last_anomaly_result())


# Example 4: display the anomalies

    anomaly_finder_app.show_anomaly_map(True)  # set false if the map should not be displayed
    anomaly_finder_app.show_anomaly_overlay(True)  # displays the anomaly overlay in the result image


# Example 5: save the required images in the specified files (jpg, jpeg, bmp oder png format -> jpeg by default)

    # the anomaly map must be activated to download
    anomaly_finder_app.save_anomaly_map('./anomalyImage.jpg')
    anomaly_finder_app.save_anomaly_map('./anomalyImage.bmp')
    anomaly_finder_app.save_anomaly_map('./anomalyImage.png')

    anomaly_finder_app.save_result_image('./resultImage.jpg')
    anomaly_finder_app.save_result_image('./resultImage.bmp')
    anomaly_finder_app.save_result_image('./resultImage.png')
