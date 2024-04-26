import json
from utils.dto.roi_object import RoiObject


class RoiConfig:
    """A Data Transfer Object to encapsulate the data of a ROI Configuration.

        Used by the Vision App Classes to add / delete ROIs to the config.

        Once fully configured it should be uploaded via the REST connection to the camera by calling the set_roi_config
        in the individual Vision App Class.

        Can be converted from / to json. """
    def __init__(self, roi_config: [RoiObject]):
        self.roi_config = roi_config

    @classmethod
    def from_json(cls, data: json):
        return RoiConfig(data["rois"])

    def add_roi(self, new_roi: RoiObject):
        self.roi_config.append(new_roi)

    def delete_roi(self, roi: RoiObject):
        self.roi_config.remove(roi)

    def get_config(self):
        for roi in self.roi_config:
            print(roi.to_json())

    def get_roi(self, roi_name: str) -> RoiObject:
        for RoiObject in self.roi_config:
            if RoiObject.identifier == roi_name:
                return RoiObject

    def to_map(self) -> dict:
        roi_config_json = []
        for roi in self.roi_config:
            json_roi = roi.to_json()
            # json_roi["CenterX"] = json_roi["OffsetX"]
            # del json_roi["OffsetX"]
            # json_roi["CenterY"] = json_roi["OffsetY"]
            # del json_roi["OffsetY"]
            roi_config_json.append(json_roi)
        return {"rois": roi_config_json}

    #save to file

    #load to file

