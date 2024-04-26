import json


class CameraRoi:
    """A Data Transfer Object to specify the data of a Sensor ROI (OffsetX, OffsetY, Width, Height) which is
        used to limit the image directly on the sensor before processing.

        Used by NxtCameraHandler Class for configuration purposes.

        Can be converted from / to json.

        NOTE: affects ROI Configuration within the Vision App."""

    def __init__(self, offset_x: int = None, offset_y: int = None, width: int = None, height: int = None):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height

    def __str__(self):
        return f"OffsetX:{self.offset_x} OffsetY:{self.offset_y} Width:{self.width} Height:{self.height}"

    @classmethod
    def from_json(cls, data: json):
        return CameraRoi(data["OffsetX"], data["OffsetY"], data["Width"], data["Height"])

    def to_json(self) -> dict:
        return {"OffsetX": self.offset_x,
                "OffsetY": self.offset_y,
                "Width": self.width,
                "Height": self.height}
