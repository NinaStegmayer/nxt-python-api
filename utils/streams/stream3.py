import json
from enum import Enum
from utils.streams.stream_parent import StreamParent


class Stream3(StreamParent):
    """Inherits from StreamParent.

        Height, ReadOnly, URL and Width are not writeable parameters."""

    class RESOLUTION(Enum):
        FULL_HD = "FULL_HD"
        HD = "HD"
        r1440X1080 = "1440X1080"
        WQHD = "WQHD"

    def __init__(self):
        super().__init__()

    def from_json(self, data: json):
        self.EncodingType = Stream3.ENCODINGTYPE(data["EncodingType"])
        self.Framerate = data["Framerate"]
        self.H26xBitrateMode = Stream3.H26XBITRATEMODE(data["H26xBitrateMode"])
        self.H26xKeyFrameInterval = data["H26xKeyFrameInterval"]
        self.H26xTargetBitrate = data["H26xTargetBitrate"]
        self._Height = data["Height"]
        self.MJPEGQuality = data["MJPEGQuality"]
        self._ReadOnly = data["ReadOnly"]
        self.Resolution = Stream3.RESOLUTION(data["Resolution"])
        self._URL = data["URL"]
        self._Width = data["Width"]
        return self
