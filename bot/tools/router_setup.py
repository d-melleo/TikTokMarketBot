from typing import Any, List, Type, Optional, Set, Tuple

from aiogram import BaseMiddleware, Dispatcher, Router
from aiogram.enums import UpdateType
from aiogram.filters import MagicData
from aiogram.utils.magic_filter import MagicFilter


def _resolve_event_names(include_events, exclude_events) -> List[str]:
    if (include_events and exclude_events) or include_events:
        # Return passed events by user
        return include_events
    elif exclude_events:
        # Return all events, except the events in exclude list
        return [x.value for x in UpdateType if x.value not in exclude_events]
    else:
        # If both lists are empty or None, return all events
        return [x.value for x in UpdateType]

def register_filters(
    router: Dispatcher | Router,
    filters: Set[MagicData | MagicFilter | Any],
    include_events: Optional[List[str]] = None,
    exclude_events: Optional[List[str]] = None
) -> None:
    """
    Register filters for specified events on the given router.
    
    - If both `include_events` and `exclude_events` are empty or None, 
        defaults to all events.
    
    :param router: Router or Dispatcher instance.
    :param filters: Set of positional filters.
    :param include_events: List of events to include; will always override `exclude_events`.
    :param exclude_events: List of events to exclude; used if no `include_events` are provided.
    """
    events = _resolve_event_names(include_events, exclude_events)

    for observer_name, observer_event in router.observers.items():
        if observer_name in events:
            observer_event.filter(*filters)

def register_middlewares(
    router: Dispatcher | Router,
    inner: Optional[Tuple[Type[BaseMiddleware]]] = None,
    outer: Optional[Tuple[Type[BaseMiddleware]]] = None,
    include_events: Optional[List[str]] = None,
    exclude_events: Optional[List[str]] = None
) -> None:
    """
    Register inner and outer middlewares for specified events on the given router.
    
    - If both `include_events` and `exclude_events` are empty or None, 
        defaults to all events.
    - Middlewares execute in the order they are registered and are registered
        in the order they appear in the `inner` and `outer` tuples.
    
    :param router: Router or Dispatcher instance.
    :param inner: Tuple of inner middlewares to register.
    :param outer: Tuple of outer middlewares to register.
    :param include_events: List of events to include; will always override `exclude_events`.
    :param exclude_events: List of events to exclude; used if no `include_events` are provided.
    """
    events = _resolve_event_names(include_events, exclude_events)

    for observer_name, observer_event in router.observers.items():
        if observer_name in events:
            
            if outer:
                for outer_middleware in outer:
                    observer_event.outer_middleware(outer_middleware())
            if inner:
                for inner_middleware in inner:
                    observer_event.middleware(inner_middleware())