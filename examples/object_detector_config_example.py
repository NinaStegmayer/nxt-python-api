from config.nxt_config import NXTConfig
from logs.logger import nxt_logger
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_object_detector import NXTVAppObjectDetector
from utils.dto.roi_config import RoiConfig
from utils.dto.roi_object import RoiObject

if __name__ == "__main__":

    CNN_PATH = r"{absolute path from your directory to required CNN}"
    """requires absolute path of the CNN with file ending .rdet for IDS NXT rio / .mdet for IDS NXT malibu"""

    CNN_NAME = 'your_cnn'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to Object Detector Vision App}"
    """requires absolute path of the Vision App with file ending .vapp"""

    config = NXTConfig()
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)
    object_detector_app = NXTVAppObjectDetector(rest_connection)

    object_detector_app.vapp_handler.setup_vapp(VAPP_PATH, object_detector_app.vapp)

    # configure the required CNN
    if CNN_NAME not in object_detector_app.get_available_cnns():
        object_detector_app.install_cnn(CNN_PATH)

    object_detector_app.set_current_cnn(CNN_NAME)

    # configure ROIs
    roiconfig = RoiConfig([])

    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_1", 300))
    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_2", 200))
    roiconfig.add_roi(RoiObject(0, 200, 200, 300, "roi_3", 400))

    object_detector_app.set_roiconfig(roiconfig)

    # modify specific parameters of a ROI (.width / .height / .identifier / .angle / .centerX / .centerY)
    roiconfig.get_roi("roi_1").width = 500

    # delete ROI
    object_detector_app.delete_single_roi("roi_2", roiconfig)

    # print current ROI configuration
    roiconfig.get_config()

    # configure threshold
    object_detector_app.set_threshold(60)

    # display result image
    object_detector_app.show_result_image(True)

    # save and log results
    object_detector_app.save_result_image('./resultImage.jpg')
    nxt_logger.info(object_detector_app.get_last_detection_resultsources())  # returns the results
    nxt_logger.info(object_detector_app.get_result_highlight())  # returns the result highlights

