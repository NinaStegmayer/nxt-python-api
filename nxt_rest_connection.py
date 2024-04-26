import ssl
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode
from enum import Enum
from utils.dto.rest_result import RestResult



class NXTRestConnection:
    """Creates REST connection and provides general HTTP request methods"""
    header_base = {}

    class HttpContentTypes(Enum):
        ApplicationXWwwFormUrlencoded = 'application/x-www-form-urlencoded'
        ApplicationOctetStream = 'application/octet-stream'
        ApplicationVapp = 'application/vapp'
        ApplicationJson = 'application/json'
        ImageJpeg = 'image/jpeg'
        ImageBmp = 'image/bmp'
        ImagePng = 'image/png'

    class HttpAccept(Enum):
        ImageJpeg = 'image/jpeg'
        ImageBmp = 'image/bmp'
        ImagePng = 'image/png'

    def __init__(self, ip: str, username: str, password: str, use_ssl=False):

        self.request = urllib.request
        self.ip = ip
        self.ssl_ctx = None

        if use_ssl:
            self.baseurl = f"https://{self.ip}"
            # disable ssl certificate check
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            self.baseurl = f"http://{self.ip}"

        self.init_connection(username, password)

    def init_connection(self, username: str, password: str):
        b64_authorisation = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")
        self.header_base['Authorization'] = 'Basic %s' % b64_authorisation

        # needed to disable Corporate Proxy....
        proxy_handler = self.request.ProxyHandler({})

        # create "opener" (OpenerDirector instance)
        opener = self.request.build_opener(proxy_handler)

        # Install the opener.
        # Now all calls to urllib.request.urlopen use our opener.
        self.request.install_opener(opener)

    def __base_request(self, request_type: RestResult.RequestType, path: str,
                       content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
                       params: dict = None,
                       additional_headers: dict = None,
                       data=None,
                       timeout=5) -> RestResult:

        this_result = RestResult(path, request_type)

        url = f"{self.baseurl}{path}"
        # nxt_logger.info(f"Base Request to {url}")
        if params:
            urlencoded_params = urllib.parse.urlencode(params)
            url += f"?{urlencoded_params}"
            print(url)

        header = self.header_base
        header['Content-Type'] = str(content_type.value)
        header['accept'] = str(content_type.value)
        header['Accept'] = str(content_type.value)

        if additional_headers:
            header.update(additional_headers)
        req = self.request.Request(url, headers=header, method=str(request_type.value))
        try:
            with self.request.urlopen(req, data=data, timeout=timeout, context=self.ssl_ctx) as response:
                this_result.response_data = response.read()
                this_result.response_status = response.status
                this_result.response_header = response.headers
        except urllib.error.HTTPError as e:
            msg_body = e.read()
            raise Exception(f"Request failed: StatusCode: {e.status} Reason: {msg_body}")

        if this_result.response_status != 200:
            raise Exception(
                f"Request failed: StatusCode: {this_result.response_status} Reason: {this_result.response_data}")

        return this_result

    def get(self, path: str, content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
            params: dict = None,
            additional_headers: dict = None) -> RestResult:

        return self.__base_request(RestResult.RequestType.GET, path, content_type, params, additional_headers)

    def patch(self, path: str,
              content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
              params: dict = None,
              additional_headers: dict = None
              ) -> RestResult:
        data = urllib.parse.urlencode(params).encode('utf-8')
        params.clear()
        return self.__base_request(RestResult.RequestType.PATCH, path, content_type, params,
                                   additional_headers, data)

    def post(self, path: str,
             content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
             params: dict = None,
             additional_headers: dict = None
             ) -> RestResult:
        return self.__base_request(RestResult.RequestType.POST, path, content_type, params, additional_headers)

    def put(self, path: str,
            content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
            params: dict = None,
            additional_headers: dict = None,
            data=None
            ) -> RestResult:
        return self.__base_request(RestResult.RequestType.PUT, path, content_type, params, additional_headers, data)

    def delete(self, path: str,
               content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
               params: dict = None,
               additional_headers: dict = None
               ) -> RestResult:
        return self.__base_request(RestResult.RequestType.DELETE, path, content_type, params, additional_headers)

    def options(self, path: str,
                content_type=HttpContentTypes.ApplicationXWwwFormUrlencoded,
                params: dict = None,
                additional_headers: dict = None
                ) -> RestResult:
        return self.__base_request(RestResult.RequestType.OPTIONS, path, content_type, params, additional_headers)

    @staticmethod
    def get_image_accept_header_by_filename(filename: str) -> HttpAccept:
        if filename.casefold().endswith('.jpg') or filename.casefold().endswith('.jpeg'):
            return NXTRestConnection.HttpAccept.ImageJpeg
        elif filename.casefold().endswith('.bmp'):
            return NXTRestConnection.HttpAccept.ImageBmp
        elif filename.casefold().endswith('.png'):
            return NXTRestConnection.HttpAccept.ImagePng
        else:
            raise Exception("Imageformat not valid. Only jpg, jpeg, bmp and png are supported.")

    @staticmethod
    def get_image_content_type_by_filename(filename: str) -> HttpContentTypes:
        if filename.casefold().endswith('.jpg') or filename.casefold().endswith('.jpeg'):
            return NXTRestConnection.HttpContentTypes.ImageJpeg
        elif filename.casefold().endswith('.bmp'):
            return NXTRestConnection.HttpContentTypes.ImageBmp
        elif filename.casefold().endswith('.png'):
            return NXTRestConnection.HttpContentTypes.ImagePng
        else:
            raise Exception("Imageformat not valid. Only jpg, bmp and png are supported.")
