"""
Meeting problem:

Two people with a very busy calendar are trying to meet today.

Write an algorithm that takes two people calendars returning free slots of time
during these two people may meet.

Input:

* Two calendars with the slots currently taken today for both people.
* Daily bounds.
* Meeting duration.

Output: A list of slots in which they may meet.

This problem was taken from this video, but with a different implementation:

https://www.youtube.com/watch?v=kbwk1Tw3OhE

See the find_available_slots docstring and the tests.py file if you want to
know how to use it.
"""

from datetime import date, time, timedelta
from datetime import datetime as dt


def find_available_slots(calendar1, calendar2, bounds, min_slot=30):
    """
    Return the available slots of time from two calendars,
    the daily bounds and the meeting duration in minutes. Example::

    >>> calendar1 = [('10:00', '10:40'), ('12:00', '12:30')]
    >>> calendar2 = [('11:20', '11:50'), ('12:00', '12:45')]
    >>> bounds = ('9:00', '14:00')
    >>> find_available_slots(calendar1, calendar2, bounds, 30)
    [('09:00', '10:00'), ('10:40', '11:20'), ('12:45', '14:00')]
    """
    start, end = _slot_to_time(bounds)
    calendar1 = list(map(_slot_to_time, calendar1))
    calendar2 = list(map(_slot_to_time, calendar2))
    t = start
    slots = []
    while t < end and (calendar1 or calendar2):
        slot1 = calendar1[0] if calendar1 else (None, None)
        slot2 = calendar2[0] if calendar2 else (None, None)
        tmin = _min_time(slot1[0], slot2[0])
        d = date.today()
        if dt.combine(d, t) < dt.combine(d, tmin) - timedelta(minutes=min_slot):
            # enough time to schedule a meeting
            slots.append((t, tmin))

        # move to the next time
        t = _min_time(slot1[1], slot2[1])

        # remove consumed slots from any calendar
        if t and t == slot1[1]:
            calendar1.pop(0)
        if t and t == slot2[1]:
            calendar2.pop(0)
    if dt.combine(d, t) < dt.combine(d, end) - timedelta(minutes=min_slot):
        slots.append((t, end))

    return [(_time_to_str(t1), _time_to_str(t2)) for t1, t2 in slots]


# Auxiliar functions

def _str_to_time(s):
    hour, minute = s.split(':')
    return time(int(hour), minute=int(minute))


def _slot_to_time(slot):
    return tuple(map(_str_to_time, slot))


def _time_to_str(d):
    return d.strftime('%H:%M')


def _min_time(t1, t2):
    return min(t1, t2) if t1 and t2 else t1 or t2
