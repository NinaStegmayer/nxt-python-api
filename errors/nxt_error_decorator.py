from urllib.error import HTTPError


def nxt_error_decorator(func):
    def inner():
        try:
            func()
        except HTTPError as e:
            e.read()
