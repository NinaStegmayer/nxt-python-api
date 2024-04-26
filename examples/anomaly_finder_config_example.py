from config.nxt_config import NXTConfig
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_anomaly_finder import NXTVAppAnomalyFinder
from logs.logger import nxt_logger

if __name__ == "__main__":

    config = NXTConfig()

    CNN_PATH = r"{absolute path from your directory to required CNN}"
    """requires absolute path to the CNN with file ending 
        .rano for IDS NXT rio Cameras / .mano for IDS NXT malibu Cameras"""

    CNN_NAME = 'your_cnn'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to anomaly finder vision app}"
    """requires absolute path of the Vision App with file ending .vapp"""

    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    anomaly_finder_app = NXTVAppAnomalyFinder(rest_connection)

    anomaly_finder_app.vapp_handler.setup_vapp(VAPP_PATH, anomaly_finder_app.vapp)

    if CNN_NAME not in anomaly_finder_app.get_available_cnns():
        anomaly_finder_app.install_cnn(CNN_PATH)

    anomaly_finder_app.set_current_cnn(CNN_NAME)

    anomaly_finder_app.set_threshold(70)

    anomaly_finder_app.show_anomaly_map(True)
    anomaly_finder_app.show_anomaly_overlay(True)
    nxt_logger.info(anomaly_finder_app.get_last_anomaly_result())

    anomaly_finder_app.save_anomaly_map('./anomalyImage.jpg')
    anomaly_finder_app.save_result_image('./resultImage.jpg')
