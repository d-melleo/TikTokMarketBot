from enum import Enum


class PrivateChatMarkupData(str, Enum):
    # Start button
    SEND_VIDEO_DATA = "send_video"
    # Languages
    EN_LANGUAGE_DATA = "en"
    PL_LANGUAGE_DATA = "pl"
    UK_LANGUAGE_DATA = "uk"