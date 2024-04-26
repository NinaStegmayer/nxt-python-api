# The following code is required for each example:
from config.nxt_config import NXTConfig
from logs.logger import nxt_logger # this import allows to use the project logger
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_object_detector import NXTVAppObjectDetector


if __name__ == "__main__":
    CNN_PATH = r"{path from your directory to required CNN}"
    """requires absolute path of the CNN with file ending .rdet for IDS NXT rio / .mdet for IDS NXT malibu"""

    CNN_NAME = 'your_cnn'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to object detector vision app}"
    """requires absolute path of the Vision App with file ending .vapp"""

    # generates new configuration of parameters defined in the config/config.ini
    config = NXTConfig()

    # establishes RestConnection with parameters defined in /config/config.ini
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    # creates an object of the Vision App
    object_detector_app = NXTVAppObjectDetector(rest_connection)

    # Deactivates running Vision Apps then installs and activates given Vision App
    object_detector_app.vapp_handler.setup_vapp(VAPP_PATH, object_detector_app.vapp)

# Example 1: configure the required CNN

    # display and log the CNNs already installed
    nxt_logger.info(object_detector_app.get_available_cnns())

    # if the required CNN is not already installed you need to install it
    # (*.rdet (for IDS NXT rio), *.mdet (for IDS NXT malibu), *.det):
    object_detector_app.install_cnn(CNN_PATH)  # specify the path of the CNN: keep in mind that it needs to be a valid name!

    # specify the required CNN:
    object_detector_app.set_current_cnn(CNN_NAME)  # enter name of the CNN

    # delete the current CNN:
    object_detector_app.delete_active_cnn()


# Example 2: configure the required threshold

    object_detector_app.set_threshold(60)


# Example 3: create Regions of interest (ROI) - the two following imports are required
    from utils.dto.roi_config import RoiConfig
    from utils.dto.roi_object import RoiObject

    # generate a new configuration to which the created ROIs need to be added
    roiconfig = RoiConfig([])

    # create required ROIs and add those to the previous generated configuration
    roi_1 = RoiObject(0, 200, 200, 200, "roi_1", 300)
    roiconfig.add_roi(roi_1)
    # or like this
    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_2", 200))

    # now upload / update the ROI config to the camera
    object_detector_app.set_roiconfig(roiconfig)

# 3.x: further options for ROIs
    # 3.1 print and logs the current ROI configuration
    nxt_logger.info(roiconfig.get_config())
    # 3.2 print and logs position of single ROIs
    nxt_logger.info(object_detector_app.gets_single_roi_position("roi_2"))
    # 3.3 modify specific parameters of a ROI (.width / .height / .identifier / .angle / .centerX / .centerY)
    roiconfig.get_roi("roi_1").width = 500
    roiconfig.get_roi("roi_2").height = 250

    # setting RoiConfig is required to PATCH changes to the camera!
    object_detector_app.set_roiconfig(roiconfig)

    # 3.4 delete a single ROI
    object_detector_app.delete_single_roi("roi_1", roiconfig)


# Example 4: display the results

    object_detector_app.show_result_image(True)  # displays the result image - set false if the result image should not be displayed

    # the result image must be activated to download
    object_detector_app.save_result_image('./resultImage.jpg')  # saves current result image in the specified file (jpg, jpeg, bmp oder pnb format -> jpeg by default)

    nxt_logger.info(object_detector_app.get_last_detection_resultsources())  # returns the results
    nxt_logger.info(object_detector_app.get_result_highlight())  # returns the result highlights







