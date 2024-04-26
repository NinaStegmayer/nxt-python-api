class VisionAppError(Exception):
    def __init__(self):
        self.message = ""

    def __str__(self):
        return self.message


class ResultImageNotFound(VisionAppError):
    def __init__(self, flag_name: str):
        self.message = f"Set the configurable result image flag {flag_name} to True"


class AttentionMapNotAvailable(VisionAppError):
    def __init__(self):
        self.message = "The current CNN does not support the feature of the attention map "
