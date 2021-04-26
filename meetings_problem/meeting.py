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

from datetime import datetime, timedelta


__all__ = ['find_available_slots']


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
    start, end = _slot_to_date(bounds)
    calendar1 = list(map(_slot_to_date, calendar1))
    calendar2 = list(map(_slot_to_date, calendar2))
    d = start
    slots = []
    while d < end and (calendar1 or calendar2):
        slot1 = calendar1[0] if calendar1 else (None, None)
        slot2 = calendar2[0] if calendar2 else (None, None)
        dmin = _min_date(slot1[0], slot2[0])
        if d < dmin - timedelta(minutes=min_slot):
            # enough time to schedule a meeting
            slots.append((d, dmin))

        # move to the next time
        d = _min_date(slot1[1], slot2[1])

        # remove consumed slots from any calendar
        if d and d == slot1[1]:
            calendar1.pop(0)
        if d and d == slot2[1]:
            calendar2.pop(0)
    if d < end - timedelta(minutes=min_slot):
        slots.append((d, end))

    return [(_date_to_str(d1), _date_to_str(d2)) for d1, d2 in slots]


# Auxiliar functions

def _str_to_date(s):
    hour, minute = s.split(':')
    return datetime.now().replace(
        hour=int(hour), minute=int(minute), second=0, microsecond=0,
    )


def _slot_to_date(slot):
    return tuple(map(_str_to_date, slot))


def _date_to_str(d):
    return d.strftime('%H:%M')


def _min_date(d1, d2):
    return min(d1, d2) if d1 and d2 else d1 or d2
