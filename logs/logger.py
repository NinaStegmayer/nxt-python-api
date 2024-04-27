import logging
import platform
import sys

"""
    asctime - time stamp with passed format %Y-%m-%dT%H:%M:%S%z
    levelname - INFO, WARN, ERROR
    message - log message
    name - file name and line that led to log entry
"""
# same format as in django...
LOGGING_FORMATTER = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(thread)d - %(message)s',
                                      "%d/%b/%Y %H:%M:%S")


# Logging is done in three files
# backend.log -> container for ALL logs on debug level
# component.log -> container for ALL logs for a SINGLE COMPONENT on debug level
# in addition, everything is output in a stream handler

class NXTLogger:

    def __init__(self, component="NXT"):
        self.component = component
        if platform.system() == 'Linux':
            self.log_dir = "/var/log/nxt"
        elif platform.system() == 'Windows':
            self.log_dir = "../logs"
        else:
            self.log_dir = "../logs"
        logger = logging.getLogger(self.component)
        logger.setLevel(logging.DEBUG)

        handles = [{"file": f"{self.log_dir}/nxt.log", "level": logging.DEBUG}]

        for handle in handles:
            # create file for component log
            component_file_handler = logging.FileHandler(handle.get("file"))
            component_file_handler.setLevel(handle.get("level"))
            component_file_handler.setFormatter(LOGGING_FORMATTER)
            logger.addHandler(component_file_handler)

        # create logging for stream output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(LOGGING_FORMATTER)
        logger.addHandler(stream_handler)

        self.logger = logger

    def get_logger(self):
        return self.logger


nxt_logger = NXTLogger().get_logger()
