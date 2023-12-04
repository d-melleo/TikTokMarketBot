"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""

from textwrap import dedent

from aiogram.utils.i18n import gettext as _
from emoji import emojize

from ...enums import AdmissionsChannelMarkupData as MD


def start() -> str:
    return dedent(_(
"""\
Hello {}!

Here, you can sell your video that lasts up to 60 seconds.
The video should be entertaining, similar to Tik-Tok, and created by you personally.

If we like the video, we will contact you. {}{}{}\
""")).format(
    emojize(':smiling_face_with_sunglasses:'),
    emojize(':backhand_index_pointing_left:'),
    emojize(':winking_face_with_tongue:'),
    emojize(':backhand_index_pointing_left:')
)


def banned() -> str:
    return dedent(_(
"""\
Sorry, but you cannot send messages at the moment. {}\
""")).format(
    emojize(':face_with_medical_mask:')
)


def on_hold(days: int, hours: int, minutes: int, seconds: int) -> str:
    return dedent(_(
"""\
{emoji} We are still reviewing your previous video. Once reviewed, you will be able to send us more. \
Or, after{days}d{hours}h{minutes}m, if we don't complete the review by the time.\
""")).format(
    emoji=emojize(':see-no-evil_monkey:'),
    days=f' {days}' if days else '',
    hours= ' {hours}' if hours else '',
    minutes=f' {minutes}' if seconds > 60 else ' 1')


def request_video() -> str:
    return dedent(_(
"""\
Send your video up to 60 seconds:\
"""))


def received_video() -> str:
    return dedent(_(
"""\
{} Thank you! We will review your video and respond to you shortly.\
""")).format(
    emojize(':check_box_with_check:')
)


def received_video_long() -> str:
    return dedent(_(
"""\
{} You can send one video at a time with a duration of up to 60 seconds.\
""")).format(
    emojize(':cross_mark:')
)


def received_other_media() -> str:
    return dedent(_(
"""\
{} We only accept video submissions.\
""")).format(
    emojize(':cross_mark:')
)


def notify_user_desicion(decision: str) -> str:
    if decision == MD.CONFIRMED_LIKED_DATA:
        return """\
Congratulations! Your video was a hit!
We'll be reaching out to you very soon to dive into further discussions.\
"""
    elif decision == MD.CONFIRMED_DISLIKED_DATA:
        return """\
Hey, thanks a bunch for your recent video! \
Although we've decided not to move forward with it this time, \
we're super excited to see more of your content!\
"""