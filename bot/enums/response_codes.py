from enum import Enum


class Response(int, Enum):
    CONTINUE = 100
    OK = 200
    NOT_MODIFIED = 304
    NOT_FOUND = 404