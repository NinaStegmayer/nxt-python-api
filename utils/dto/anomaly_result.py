import json


class AnomalyResult:
    """ Encapsulates the results of the Anomaly Finder examination (Anomaly, Anomaly Score, Inference Time).

        Data Transfer Object can be converted from json."""
    def __init__(self, anomaly: bool, anomaly_score: float, inference_time_ms: int):
        self.anomaly = anomaly
        self.anomaly_score = anomaly_score
        self.inference_time_ms = inference_time_ms

    @classmethod
    def from_json(cls, data: json):
        return AnomalyResult(data["anomaly"], data["score"], data["inferencetime"])

    def __str__(self):
        return f"Anomaly:{self.anomaly} Score: {self.anomaly_score} InferenceTime: {self.inference_time_ms}"
