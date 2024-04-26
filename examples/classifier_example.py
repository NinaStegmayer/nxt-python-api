# The following code is required for each example:
from config.nxt_config import NXTConfig
from logs.logger import nxt_logger # this import allows to use the project logger
from nxt_rest_connection import NXTRestConnection
from vapps.nxt_vapp_classifier import NXTVAppClassifier

if __name__ == "__main__":
    config = NXTConfig()
    CNN_PATH = r"{path from your directory to required CNN}"
    """requires absolute path of the CNN with file ending .rcla for IDS NXT rio / .mcla for IDS NXT malibu"""

    CNN_NAME = 'your_cnn'
    "Name of the CNN as String."

    VAPP_PATH = r"{path from your directory to classifier vision app}"
    """requires absolute path of the Vision App with file ending .vapp"""

    # establishes RestConnection with parameters defined in /config/config.ini
    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    # creates an object of the Vision App
    classifier_app = NXTVAppClassifier(rest_connection)

    # Deactivates running Vision Apps then installs and activates given Vision App
    classifier_app.vapp_handler.setup_vapp(VAPP_PATH, classifier_app.vapp)

# Example 1: configure the required CNN

    # display and logs the CNNs already installed
    nxt_logger.info(classifier_app.get_available_cnns())

    # if the required CNN is not already installed you need to install it
    # (*.rcla (for IDS NXT rio), *.mcla(for IDS NXT malibu), *.cnn):
    classifier_app.install_cnn(CNN_PATH)  # specify the path of the CNN: keep in mind that it needs to be a valid name!

    # specify the required CNN:
    classifier_app.set_current_cnn(CNN_NAME)  # enter name of the CNN

    # delete the current CNN:
    classifier_app.delete_active_cnn()

# Example 2: create Regions of interest (ROI) - the two following imports are required
    from utils.dto.roi_config import RoiConfig
    from utils.dto.roi_object import RoiObject

    # generate a new configuration to which the created ROIs need to be added
    roiconfig = RoiConfig([])

    # create required ROIs and add those to the previous generated configuration
    # YOU NEED TO PATCH LATER with .set_roiconfig !
    roi_1 = RoiObject(0, 200, 200, 200, "roi_1", 300)
    roiconfig.add_roi(roi_1)
    # or like this
    roiconfig.add_roi(RoiObject(0, 200, 200, 200, "roi_2", 200))

    # now upload / update the ROI config to the camera !REQUIRED!
    classifier_app.set_roiconfig(roiconfig)

    # 2.x: further options for ROIs
    # 2.1 print and log the current ROI configuration
    nxt_logger.info(roiconfig.get_config())
    # 2.2 print and log position of single ROIs
    nxt_logger.info(classifier_app.gets_single_roi_position("roi_2"))
    # 2.3 modify specific parameters of a ROI (.width / .height / .identifier / .angle / .centerX / .centerY)
    roiconfig.get_roi("roi_1").width = 500
    roiconfig.get_roi("roi_2").height = 250
    # - afterward upload config to the camera !REQUIRED!
    classifier_app.set_roiconfig(roiconfig)
    # 2.4 delete a single ROI
    classifier_app.delete_single_roi("roi_1", roiconfig)


# Example 3: display the results
    classifier_app.show_attention_map(True)  # displays the attention map - set false if you want to hide the attention map

    nxt_logger.info(classifier_app.get_last_detection_resultsources())  # returns the results

# Example 4: save the current result image in the specified file (jpg, jpeg, bmp oder png format)
    classifier_app.save_result_image('./result_image')  # converts to jpeg by default

    # the attention map must be activated to download
    classifier_app.save_attention_map('./attention_map.jpg')


# Example 5: open website
    classifier_app.get_website()

