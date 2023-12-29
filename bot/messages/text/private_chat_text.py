"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""
from typing import Dict

from aiogram.utils.i18n import gettext as _

from . import emojies as emj
from ...enums import AdmissionsChannelMarkupData as MD
from ...enums import PrivateChatMarkupData as PMD
from ...tools.text_formatter import text_formatter

def start() -> str:
    return _("""\
Hello {}!

Here, you can sell your video that lasts up to 60 seconds.
The video should be entertaining, similar to Tik-Tok, and created by you personally.

If we like the video, we will contact you. {}{}{}\
""").format(emj.SUNGLASSES_FACE, emj.LEFT_POINT_HAND, emj.TONGUE_FACE, emj.LEFT_POINT_HAND)


def help() -> str:
    return """\
How it Works:
1. 📹 Send us your personally made video with a duration up to 60 seconds.
2. ⏳ After submission, there is a 3-hour cooldown before you can send another video, or we may review it before the cooldown expires.
3. 💌 If we like your video, we'll reach out to you with an offer!

Submission Guidelines:
- 🎬 Videos must be created personally by you.
- 🚫 Do not post the video anywhere else until we review it.
- 📅 You can send one video at a time.
- ⏰ Allow a 3-hour cooldown before submitting another video, or wait for our review.\
"""


def language() -> str:
    return _("Select your language:")


def set_language(lang_code: str) -> str:
    if lang_code == PMD.EN_LANGUAGE_DATA:
        txt = _("{emj} Set your language to English")
    elif lang_code == PMD.PL_LANGUAGE_DATA:
        txt = _("{emj} Set your language to Polish")
    elif lang_code == PMD.UK_LANGUAGE_DATA:
        txt = _("{emj} Set your language to Ukrainian")

    return txt.format(emj=emj.POSITIVE)


def banned() -> str:
    return _(
        "{} Sorry, but you cannot send messages at the moment."
    ).format(emj.MASK_FACE)


def hold_timer(hold_timeframe: Dict[str, int]) -> str:
    days_, hours_, minutes_, seconds_ = hold_timeframe.values()

    days = _(" {days}d").format(days=days_) if days_ else ""
    hours = _(" {hours}h").format(hours=hours_) if hours_ else ""
    minutes = _(" {minutes}m")

    if minutes_ in [0, "0"]:
        minutes = ""
    elif seconds_ < 60:
        minutes = minutes.format(minutes="1")
    else:
        minutes = minutes.format(minutes=minutes_)

    return f"{days}{hours}{minutes}"


def on_hold(data: Dict[str, int]) -> str:
    return _("""\
{emoji} We are still reviewing your previous video. Once reviewed, you will be able to send us more. \
Or, after{timer}, if we don't complete the review by the time.\
""").format(emoji=emj.NO_SEE_MONKEY, timer=hold_timer(data))


def request_video() -> str:
    return _(
        "{} Send your video up to 60 seconds:"
    ).format(emj.PAPERCLIP)


def received_video() -> str:
    return _(
        "{} Thank you! We will review your video and respond to you shortly."
    ).format(emj.CHECK_BOX)


def received_video_long() -> str:
    return _(
        "{} You can send one video at a time with a duration of up to 60 seconds."
    ).format(emj.NEGATIVE)


def received_other_media() -> str:
    return _(
        "{} We only accept video submissions."
    ).format(emj.NEGATIVE)


def notify_user_desicion(decision: str) -> str:
    if decision == MD.CONFIRMED_LIKED_DATA:
        return """\
Congratulations! Your video was a hit!
We'll be reaching out to you very soon to dive into further discussions."""

    elif decision == MD.CONFIRMED_DISLIKED_DATA:
        return """\
Hey, thanks a bunch for your recent video! \
Although we've decided not to move forward with it this time, \
we're super excited to see more of your content!"""