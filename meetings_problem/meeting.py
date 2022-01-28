"""
Meeting problem:

Two people with a very busy calendar are trying to meet today.

Write an algorithm that takes two people calendars returning free slots of time
during these two people may meet.

Input:

* Two calendars with the available slots for both people.
* Daily bounds.
* Meeting duration.

Output: A list of slots in which they may meet.

This problem was taken from this video, but with a different implementation:

https://www.youtube.com/watch?v=kbwk1Tw3OhE

See the find_available_slots docstring and the tests.py file if you want to
know how to use it.
"""

from datetime import date, time
from datetime import datetime as dt


class Slot:
    start: time
    end: time

    def __init__(self, start: str, end: str):
        self.start = _str_to_time(start)
        self.end = _str_to_time(end)
        assert self.start < self.end

    def __eq__(self, slot):
        return self.start == slot.start and self.end == slot.end

    def __contains__(self, slot):
        return not (self.end < slot.start or self.start > slot.end)

    def __and__(self, slot):
        """Return the shared time slot. Usage::
        >>> Slot('9:00', '10:00') & Slot('9:30', '10:30')
        [09:30-10:00]
        """
        if self not in slot:
            return None
        return Slot.fromtime(
            max(self.start, slot.start),
            min(self.end, slot.end),
        )

    def __repr__(self):
        return f'[{_time_to_str(self.start)}-{_time_to_str(self.end)}]'

    def delta(self):
        d = date.today()
        start_date = dt.combine(d, self.start)
        end_date = dt.combine(d, self.end)
        return end_date - start_date

    @classmethod
    def fromtime(cls, start: time, end: time):
        return Slot(
            _time_to_str(start),
            _time_to_str(end),
        )


class Calendar:
    slots: list[Slot]

    def __init__(self, slots: list[Slot]):
        self.slots = slots

    def __repr__(self):
        return repr(self.slots)

    def __iter__(self):
        for slot in self.slots:
            yield slot

    def __and__(self, other):
        """
        Calendar intersection. Usage::
        >>> calendar1 = Calendar([Slot('9:00', '10:00'), Slot('11:00', '12:30'), Slot('15:00', '16:30')])
        >>> calendar2 = Calendar([Slot('8:30', '9:15'), Slot('11:30', '14:00')])
        >>> calendar1 & calendar2
        [[09:00-09:15], [11:30-12:30]]
        """
        calendar1 = iter(self)
        calendar2 = iter(other)
        slots = []
        slot1, slot2 = next(calendar1), next(calendar2)
        while True:
            try:
                if slot1.end < slot2.start:
                    slot1 = next(calendar1)  # discard slot1
                    continue
                elif slot2.end < slot1.start:
                    slot2 = next(calendar2)  # discard slot2
                    continue
                slots.append(slot1 & slot2)
                if slot1.end < slot2.end:
                    slot1 = next(calendar1)
                else:
                    slot2 = next(calendar2)
            except StopIteration:
                break
        return Calendar(slots)


def find_available_slots(slots1, slots2, bounds, meeting_duration=30):
    """
    Return the available slots of time from two calendars,
    the daily bounds and the meeting duration in minutes. Example::

    >>> slots1 = [('08:00', '09:50'), ('10:00', '11:50'), ('12:00', '14:20')]
    >>> slots2 = [('08:30', '11:40'), ('13:00', '14:45')]
    >>> bounds = ('9:00', '14:00')
    >>> find_available_slots(slots1, slots2, bounds, 30)
    [('09:00', '09:50'), ('10:00', '11:40'), ('13:00', '14:00')]
    """
    # calculate the common calendar
    bounds_slot = Slot(start=bounds[0], end=bounds[1])
    calendar1 = Calendar([Slot(start, end) for start, end in slots1])
    calendar2 = Calendar([Slot(start, end) for start, end in slots2])
    common_calendar = calendar1 & calendar2
    slots = []
    for slot in iter(common_calendar):
        if slot not in bounds_slot:
            continue

        tmp_slot = Slot.fromtime(
            start=max(slot.start, bounds_slot.start),
            end=min(slot.end, bounds_slot.end),
        )
        if tmp_slot.delta().seconds >= meeting_duration * 60:
            slots.append(tmp_slot)

    return [(_time_to_str(s.start), _time_to_str(s.end)) for s in slots]


# Auxiliar functions

def _str_to_time(s):
    hour, minute = s.split(':')
    return time(int(hour), minute=int(minute))


def _time_to_str(t):
    return f'{t:%H:%M}'
