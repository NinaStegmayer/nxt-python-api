import os

from config.nxt_config import NXTConfig
from logs.logger import nxt_logger
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_classifier import NXTVAppClassifier
from utils.dto.roi_config import RoiConfig
from utils.dto.roi_object import RoiObject

if __name__ == "__main__":

    # generates new configuration of parameters defined in the config/config.ini
    config = NXTConfig()

    CNN_PATH_MAP = r"{path from your directory to CNN with map function}"
    """requires absolute path of the CNN with file ending .rcla for IDS NXT rio / .mcla for IDS NXT malibu"""

    CNN_NAME_MAP = 'your_cnn_which_provides_maps'
    "Name of the CNN as String."

    CNN_PATH_NOMAP = r"{path from your directory to required CNN without map function}"
    """requires absolute path of the CNN with file ending .rcla for IDS NXT rio / .mcla for IDS NXT malibu"""

    CNN_NAME_NOMAP = 'your_cnn_which_does_not_provides_maps'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to classifier vision app}"
    """requires absolute path of the Vision App with file ending .vapp"""

    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    classifier_app = NXTVAppClassifier(rest_connection)

    classifier_app.vapp_handler.setup_vapp(VAPP_PATH, classifier_app.vapp)

    # configure the required CNN
    if CNN_NAME_MAP not in classifier_app.get_available_cnns():
        classifier_app.install_cnn(CNN_PATH_MAP)

    if CNN_NAME_NOMAP not in classifier_app.get_available_cnns():
        classifier_app.install_cnn(CNN_PATH_NOMAP)

    classifier_app.set_current_cnn(CNN_NAME_NOMAP)

    classifier_app.delete_active_cnn()

    # display the attention map
    classifier_app.show_attention_map(True)

    # configure ROIs
    roiconfig = RoiConfig([])

    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_1", 300))
    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_2", 200))
    roiconfig.add_roi(RoiObject(0, 200, 200, 300, "roi_3", 400))

    classifier_app.set_roiconfig(roiconfig)

    # modify specific parameters of a ROI (.width / .height / .identifier / .angle / .center_x / .center_y)
    roiconfig.get_roi("roi_1").center_y = 500

    classifier_app.delete_single_roi("roi_2", roiconfig)

    roiconfig.get_config()

    # display and log the results
    nxt_logger.info(classifier_app.get_last_detection_resultsources())
    nxt_logger.info(classifier_app.get_last_detection_resultsources())

    # save the current result image & attention map in the specified file (jpg, jpeg, bmp oder pnb format)
    classifier_app.save_result_image('./result_image')  # converts to jpeg by default
    classifier_app.save_attention_map('./attention_map.jpg')

    # delete the generated image files
    os.remove('./result_image.jpeg')
    os.remove('./attention_map.jpg')
