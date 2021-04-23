from enum import Enum

import pendulum
from toggl import api


class Color(Enum):
    RED = '#FF0000'
    GREEN = '#00FF00'
    YELLOW = '#FFFF00'


class Entry:
    def __init__(self, toggl_entry: api.TimeEntry):
        self.duration = pendulum.now() - toggl_entry.start
        self.description = toggl_entry.description

    @staticmethod
    def current():
        obj = api.TimeEntry.objects.current()
        return Entry(obj) if obj is not None else None

    def is_long_running(self):
        return self.duration.total_minutes() >= 50


def format_duration(duration: pendulum.duration):
    if duration.hours > 0:
        return '%02d:%02d:%02d' % (
            duration.hours,
            duration.minutes,
            duration.remaining_seconds
        )
    else:
        return '%02d:%02d' % (
            duration.minutes,
            duration.remaining_seconds
        )


class Py3status:
    def toggl(self):
        entry = Entry.current()

        if entry is None:
            text = "No task"
            color = Color.RED
        else:
            duration_str = format_duration(entry.duration)
            text = f'{duration_str} {entry.description}'
            color = Color.YELLOW if entry.is_long_running() else Color.GREEN

        return {
            'cached_until': self.py3.time_in(4),
            'full_text': text,
            'color': color.value
        }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    config = {
        'always_show': True,
    }
    from py3status.module_test import module_test

    module_test(Py3status, config=config)
