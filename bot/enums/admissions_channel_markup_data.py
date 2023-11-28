from enum import Enum

from emoji import emojize

class AdmissionsChannelMarkupData(Enum):
    VIDEO_LIKED_DATA = "video_liked"
    VIDEO_LIKED_LABEL = emojize(":thumbs_up:")
    
    VIDEO_DISLIKED_DATA = "video_disliked"
    VIDEO_DISLIKED_LABEL = emojize(":thumbs_down:")
    
    CONFIRMED_LIKED_DATA = "confirmed_liked"
    CONFIRMED_DISLIKED_DATA = "confirmed_disliked"
    CONFIRMED_LABEL = "Так"
    
    NOT_CONFIRMED_DATA = "not_confirmed"
    NOT_CONFIRMED_LABEL = "Ні"