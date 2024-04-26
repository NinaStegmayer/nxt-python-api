import json
from enum import Enum
from errors.read_only_parameter_error import ReadOnlyParameterError


class StreamParent:
    """
    Base class for streaming settings.

    Height, ReadOnly, URL and Width are not writeable parameters."""

    class ENCODINGTYPE(Enum):
        MJPEG = "MJPEG"

    class H26XBITRATEMODE(Enum):
        """Constant (CBR) / Variable (VBR) bitrate"""
        CBR = "CBR"
        VBR = "VBR"

    class RESOLUTION(Enum):
        FULL_HD = "FULL_HD"
        HD = "HD"
        WQHD = "WQHD"

    def __init__(self):
        self.EncodingType: StreamParent.ENCODINGTYPE = None
        self.Framerate: int = None
        "Unit: frames per second"
        self.H26xBitrateMode: StreamParent.H26XBITRATEMODE = None
        "Constant (CBR) or Variable (VBR) bitrate"
        self.H26xKeyFrameInterval: int = None
        "Distance between GOP I frames. Normally set to the framerate"
        self.H26xTargetBitrate: int = None
        "Unit: kilobit per second"
        self._Height: int = None
        """Unit: pixel
        
        NOTE: read only parameter!"""
        self.MJPEGQuality: int = None
        """The image quality, on a scale from 5 (worst) to 95 (best). The default is 75.
         Values above 95 should be avoided; 100 disables portions of the JPEG compression algorithm,
         and results in large files with hardly any gain in image quality."""
        self._ReadOnly: bool = None
        """Streamsettings can be changed.
        
         NOTE: read only parameter!"""
        self.Resolution: StreamParent.RESOLUTION = None
        self._URL: str = None
        "NOTE: read only parameter!"
        self._Width: int = None
        """Unit: pixel

        NOTE: read only parameter!"""

    @property
    def Height(self):
        return self._Height

    @Height.setter
    def Height(self, value):
        raise ReadOnlyParameterError("Height can not be set. Change Resolution if changes in height are required.")

    @property
    def ReadOnly(self):
        return self._ReadOnly

    @ReadOnly.setter
    def ReadOnly(self, value):
        raise ReadOnlyParameterError("ReadOnly parameter can not be set.")

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, value):
        raise ReadOnlyParameterError("URL parameter can not be set.")

    @property
    def Width(self):
        return self._Width

    @Width.setter
    def Width(self, value):
        raise ReadOnlyParameterError("Width can not be set. Change Resolution if changes in height are required.")

    def to_json(self):
        json_dict = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    json_dict[attr] = value.value
                else:
                    json_dict[attr] = value
        return json_dict

    def from_json(self, data: json):
        """implemented by the inheriting classes (stream1 / stream2 / stream3"""
        pass


