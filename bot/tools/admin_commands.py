import functools

from aiogram.dispatcher.flags import get_flag

from ..enums import Response
from db.userdata import UserData


def resolve_response(func):
    def response_code(action_response) -> Response:
        if not isinstance(action_response, Response):
            if action_response:
                action_response = Response.OK
            else:
                action_response = Response.NOT_FOUND
        return action_response

    @functools.wraps(func)
    async def wrapper(message, **data):
        subject_user: UserData = data.get("subject_user")

        if subject_user or (get_flag(data, "subject_user") == "bypass"):
            # Execute the handler and unpack variables
            action_response, reply_text_resolver = (await func(message, **data)).values()
            # Resolve the response code
            action_response = response_code(action_response)
            # reply_text will be passed to the 'admin_command.py' middleware
            if subject_user:
                reply_text = reply_text_resolver(action_response, subject_user)
            else:
                reply_text = reply_text_resolver(action_response)
        else:
            action_response = Response.CONTINUE
            reply_text = None

        return {
            "action_response": action_response,
            "reply_text": reply_text
        }
    return wrapper