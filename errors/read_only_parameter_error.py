from logs.logger import nxt_logger


class ReadOnlyParameterError(Exception):
    def __init__(self, message):
        self.message = message
        nxt_logger.error(self.message)

    def __str__(self):
        return self.message

