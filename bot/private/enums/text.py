from textwrap import dedent

from aiogram.utils.i18n import gettext as _


"""
:pybabel commands

: pybabel init -i locales/messages.pot -d locales -D messages -l [lang code]
: pybabel extract --input-dirs=. -o locales/messages.pot
: pybabel update -d locales -D messages -i locales/messages.pot
: pybabel compile -d locales -D messages

"""



def start() -> str:
    return dedent(_(
'''\
Hello 😎!

Here, you can sell your video that lasts up to 60 seconds.
The video should be entertaining, similar to Tik-Tok, and created by you personally.

If we like the video, we will contact you. ☜(ﾟヮﾟ☜)\
'''))


def banned() -> str:
    return dedent(_(
'''\
Sorry, but you cannot send messages at the moment.\
'''))


def on_hold(days: int, hours: int, minutes: int, seconds: int) -> str:
    return dedent(_(
'''\
🙈 We are still reviewing your previous video. Once reviewed, you will be able to send us more. \
Or, after{days}{hours}{minutes}, if we don't complete the review by the time.\
''')).format(
    days = f' {days}d' if days else '',
    hours = f' {hours}h' if hours else '',
    minutes = f' {minutes}m' if seconds > 60 else ' 1m')


def request_video() -> str:
    return dedent(_(
'''\
Send your video up to 60 seconds:\
'''))


def received_video() -> str:
    return dedent(_(
'''\
✅ Thank you! We will review your video and respond to you shortly.\
'''))


def received_video_long() -> str:
    return dedent(_(
'''\
❌ You can send one video at a time with a duration of up to 60 seconds.\
'''))


def received_other_media() -> str:
    return dedent(_(
'''\
❌ We only accept video submissions.\
'''))
