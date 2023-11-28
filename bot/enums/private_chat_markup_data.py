from enum import Enum


class PrivateChatMarkupData(str, Enum):
    SEND_VIDEO_DATA = "send_video"
    SEND_VIDEO_LABEL = "Send a video"