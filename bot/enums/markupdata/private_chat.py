from enum import Enum


class MarkupData(str, Enum):
    SEND_VIDEO_DATA = "send_video"
    SEND_VIDEO_LABEL = "Send a video"