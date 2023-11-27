from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18n, I18nMiddleware

from config import WORKDIR
from db.userdata import UserData

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
        current_locale: str = await self.get_locale(data) or self.i18n.default_locale

        if self.i18n_key:
            data[self.i18n_key] = self.i18n
        if self.middleware_key:
            data[self.middleware_key] = self

        # Use the specified language context during handler execution.
        with self.i18n.context(), self.i18n.use_locale(current_locale):
            await handler(event, data)

        print("LANGUAGE OUT")

    # Get the language from the user's instance.
    async def get_locale(self, data: Dict[str, Any]) -> str:
        my_user: UserData = data['my_user']
        return my_user.language_code