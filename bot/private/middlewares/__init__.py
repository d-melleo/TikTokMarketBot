from typing import Any, Dict, Tuple, Union

from .database import DatabaseMiddleware
from .localization import LocalizationMiddleware
from .commands import CommandsMiddleware


OUTER_MIDDLEWARE_KEY = "outer"
INNER_MIDDLEWARE_KEY = "inner"


_middlewares:\
    Dict[str, Tuple[Union[
        DatabaseMiddleware,
        LocalizationMiddleware,
        CommandsMiddleware,
        Any]]
    ] = {
        OUTER_MIDDLEWARE_KEY: (
            DatabaseMiddleware,
        ),
        INNER_MIDDLEWARE_KEY: (
            LocalizationMiddleware,
            CommandsMiddleware
        )
    }