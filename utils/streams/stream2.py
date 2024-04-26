import json
from enum import Enum
from utils.streams.stream_parent import StreamParent


class Stream2(StreamParent):
    """
    Inherits from StreamParent.

    Height, ReadOnly, URL and Width are not writeable parameters."""

    class ENCODINGTYPE(Enum):
        H264 = "H264"

    class RESOLUTION(Enum):
        VGA = "VGA"

    def __init__(self):
        super().__init__()
        self.AutoOverlay: bool = None
        "Resultoverlay should be printed."

    def from_json(self, data: json):
        self.AutoOverlay = data["AutoOverlay"]
        self.EncodingType = Stream2.ENCODINGTYPE(data["EncodingType"])
        self.Framerate = data["Framerate"]
        self.H26xBitrateMode = Stream2.H26XBITRATEMODE(data["H26xBitrateMode"])
        self.H26xKeyFrameInterval = data["H26xKeyFrameInterval"]
        self.H26xTargetBitrate = data["H26xTargetBitrate"]
        self._Height = data["Height"]
        self.MJPEGQuality = data["MJPEGQuality"]
        self._ReadOnly = data["ReadOnly"]
        self.Resolution = Stream2.RESOLUTION(data["Resolution"])
        self._URL = data["URL"]
        self._Width = data["Width"]
        return self
