from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram.enums import MessageEntityType
from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18n, I18nMiddleware

from ..enums.admissions_channel_flags import AdmissionsChannelFlags as AF
from ..middlewares.database import CURRENT_UTC_TIME_KEY
from config.environment_vars import WORKDIR
from db.userdata import UserData, get_my_user

PATH = WORKDIR/"locales"  # Path to the root directory.
DEFAULT_LOCALE = "en"  # Default language.
DOMAIN = "messages"  # i18n Domain.

# Create i18n instance for localization.
i18n = I18n(path=PATH, default_locale=DEFAULT_LOCALE, domain=DOMAIN)


# Middleware that selects a language for a user.
class LocalizationMiddleware(I18nMiddleware):
    def __init__(self) -> None:
        super().__init__(i18n)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        print("LANGUAGE IN")

        my_user: UserData = None

        # Resolve i18n for messaged to end users originated from Admissions channel
        i18n_admissions: bool = get_flag(data, AF.I18N_ADMISSIONS)
        
        if i18n_admissions:
            for entity in event.message.caption_entities:
                if entity.type == MessageEntityType.TEXT_MENTION:
                    video_from_user: User = entity.user
                    my_user: UserData = await get_my_user(video_from_user, data.get(CURRENT_UTC_TIME_KEY))
        else: # For private chat messages, user data is resovled in the database middleware
            my_user: UserData = data.get("my_user")

        # For private chat messages
        current_locale: str = await self.get_locale(my_user) or self.i18n.default_locale

        if self.i18n_key:
            data[self.i18n_key] = self.i18n
        if self.middleware_key:
            data[self.middleware_key] = self

        # Use the specified language context during handler execution.
        with self.i18n.context(), self.i18n.use_locale(current_locale):
            await handler(event, data)

        print("LANGUAGE OUT")

    # Get the language from the user's instance.
    async def get_locale(self, my_user: UserData) -> str:
        return my_user.language_code