import datetime
import json
from datetime import datetime
from enum import Enum


class RestResult:
    class RequestType(Enum):
        NONE = 'None'
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        PATCH = 'PATCH'
        DELETE = 'DELETE'
        OPTIONS = 'OPTIONS'

    def __init__(self, path: str = None, request_type: RequestType = None, params: dict = None):
        self.path = path
        self.type = request_type
        self.params = params
        self.response_data = None
        self.response_status = None
        self.response_header = None

    def __str__(self):
        return f"Status: {self.response_status}\nData Size: {len(self.response_data)} Bytes\nDate: {self.response_data}"

    def to_json(self) -> json:
        return json.loads(self.response_data)

    def get_response_data(self) -> bytes:
        return self.response_data

    def get_etag(self) -> str:
        return self.response_header.get("Etag")

    def get_date(self) -> datetime:
        date = self.response_header.headers.get("Date")
        # Format: Mon, 19 Feb 2024 15:40:23 GMT
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
