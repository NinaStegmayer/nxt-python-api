from nxt_rest_connection import NXTRestConnection
from nxt_streaming_handler import NXTStreamingHandler
from config.nxt_config import NXTConfig
from utils.streams.stream1 import Stream1


if __name__ == "__main__":

    config = NXTConfig()

    rest_connection = NXTRestConnection(config.ip, config.user, config.password)

    nxt_streaming_handler = NXTStreamingHandler(rest_connection)

    #print(nxt_streaming_handler.get_available_stream_settings_info("stream1"))
    print(nxt_streaming_handler.get_available_streams())

    stream1change = Stream1()
    stream1change.Framerate = 10
    nxt_streaming_handler.set_stream_settings(stream1change)
    print(nxt_streaming_handler.get_stream1().to_json())

    nxt_streaming_handler.stream2.Framerate = 20
    nxt_streaming_handler.set_stream_settings(nxt_streaming_handler.stream2)
    print({"Stream2 ": nxt_streaming_handler.get_stream2().to_json()})





