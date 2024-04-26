from errors.streaming_handler_error import InvalidStream
from nxt_rest_connection import NXTRestConnection
from utils.streams.stream1 import Stream1
from utils.streams.stream2 import Stream2
from utils.streams.stream3 import Stream3


class NXTStreamingHandler:
    """Only available on IDS NXT malibus"""
    def __init__(self, rest_connection: NXTRestConnection):
        # SSL Connection seems to be sometimes unstable
        self.rest_connection = rest_connection
        self.stream1 = Stream1()
        self.stream2 = Stream2()
        self.stream3 = Stream3()

    def get_available_streams(self):
        options = self.rest_connection.options(f'/streaming',
                                               content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()
        return options["Objects"]

    def get_stream_settings(self, stream_name: str):
        return self.rest_connection.get(f'/streaming/{stream_name}',
                                        content_type=NXTRestConnection.HttpContentTypes.ApplicationJson).to_json()

    def get_stream_options(self, stream_name: str):
        return self.rest_connection.options(f'/streaming/{stream_name}').to_json()

    def get_available_stream_settings(self, stream_name: str):
        settings = []
        options = self.rest_connection.options(f'/streaming/{stream_name}').to_json()
        for option in options["GET"]["application/json"]["Values"]:
            settings.append(option)
        return settings

    def get_available_stream_settings_info(self, stream_name: str):
        settings_info = {}
        options = self.rest_connection.options(f'/streaming/{stream_name}').to_json()
        for option in options["GET"]["application/json"]["Values"]:
            option_dict = {}
            if "Type" in options["GET"]["application/json"]["Values"][option]:
                option_dict["Type"] = options["GET"]["application/json"]["Values"][option]["Type"]
            if "Range" in options["GET"]["application/json"]["Values"][option]:
                option_dict["Range"] = options["GET"]["application/json"]["Values"][option]["Range"]
            settings_info[option] = option_dict
        return settings_info

    def get_stream1(self) -> Stream1:
        return self.stream1.from_json(self.rest_connection.get('/streaming/stream1').to_json())

    def get_stream2(self) -> Stream2:
        return self.stream2.from_json(self.rest_connection.get('/streaming/stream2').to_json())

    def get_stream3(self) -> Stream3:
        return self.stream3.from_json(self.rest_connection.get('/streaming/stream3').to_json())

    def set_stream_settings(self, stream):
        settings_dict = {}

        if isinstance(stream, Stream1):
            stream_name = "stream1"
            if stream.AutoOverlay is not None:
                settings_dict["AutoOverlay"] = stream.AutoOverlay

        elif isinstance(stream, Stream2):
            stream_name = "stream2"
            if stream.AutoOverlay is not None:
                settings_dict["AutoOverlay"] = stream.AutoOverlay

        elif isinstance(stream, Stream3):
            stream_name = "stream3"

        else:
            raise InvalidStream()

        if stream.EncodingType is not None:
            settings_dict["EncodingType"] = stream.EncodingType
        if stream.Framerate is not None:
            settings_dict["Framerate"] = stream.Framerate
        if stream.H26xBitrateMode is not None:
            settings_dict["H26xBitrateMode"] = stream.H26xBitrateMode.value
        if stream.H26xKeyFrameInterval is not None:
            settings_dict["H26xKeyFrameInterval"] = stream.H26xKeyFrameInterval
        if stream.H26xTargetBitrate is not None:
            settings_dict["H26xTargetBitrate"] = stream.H26xTargetBitrate
        if stream.MJPEGQuality is not None:
            settings_dict["MJPEGQuality"] = stream.MJPEGQuality
        if stream.Resolution is not None:
            settings_dict["Resolution"] = stream.Resolution.value

        return self.rest_connection.patch(f'/streaming/{stream_name}',
                                          content_type=NXTRestConnection.HttpContentTypes.ApplicationJson,
                                          params=settings_dict)



