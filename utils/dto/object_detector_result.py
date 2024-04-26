import json


class ObjectDetectorResult:
    """ Encapsulates the results of the Object Detector examination (Count, Data, Detection, Highlight).

    Data Transfer Object can be converted from json."""
    def __init__(self, count: str, data: str, detection: str, highlight: str):
        self.count = count
        self.data = data
        self.detection = detection
        self.highlight = highlight

    @classmethod
    def from_json(cls, data: json):
        return ObjectDetectorResult(data["count"], data["data"], data["detection"], data["highlight"])

    def __str__(self):
        return f"Count:{self.count} Data: {self.data} Detection: {self.detection} Highlight: {self.highlight}"
