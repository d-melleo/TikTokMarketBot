from enum import Enum

class MiddlewareScope(str, Enum):
    OUTER = "outer"
    INNER = "inner"