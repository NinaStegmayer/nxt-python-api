class StreamingHandlerError(Exception):
    def __init__(self):
        self.message = ""

    def __str__(self):
        return self.message


class InvalidStream(StreamingHandlerError):
    def __init__(self):
        self.message = "Pass valid Stream Object."
