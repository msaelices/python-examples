#!/usr/bin/env python3

import unittest

from meeting import find_available_slots, Calendar, Slot


class SlotTests(unittest.TestCase):

    def test_contains(self):
        slot1 = Slot('9:00', '10:00')
        slot2 = Slot('9:30', '10:30')
        slot3 = Slot('12:00', '13:00')
        self.assertTrue(slot1 in slot2)
        self.assertTrue(slot2 in slot1)
        self.assertFalse(slot1 in slot3)

    def test_intersection(self):
        slot1 = Slot('9:00', '10:00')
        slot2 = Slot('9:30', '10:30')
        slot3 = Slot('12:00', '13:00')
        self.assertEqual(
            slot1 & slot2,
            Slot('9:30', '10:00')
        )
        self.assertIsNone(slot1 & slot3)


class CalendarTests(unittest.TestCase):

    def test_intersection(self):
        """Test the calendars intersection"""
        calendar1 = Calendar([Slot('9:00', '10:00'), Slot('11:00', '12:30'), Slot('15:00', '16:30')])
        calendar2 = Calendar([Slot('8:30', '9:15'), Slot('11:30', '14:00')])
        common_calendar = calendar1 & calendar2

        self.assertEqual(
            list(iter(common_calendar)),
            [
                Slot('09:00', '09:15'),
                Slot('11:30', '12:30'),
            ]
        )


class FindAvailableSlotsTests(unittest.TestCase):

    def test_available_slots_are_found(self):
        """Test the happy path"""
        slots1 = [
            ('08:00', '09:50'),
            ('10:00', '11:50'),
            ('12:00', '13:20'),
            ('14:00', '15:30'),
            ('17:30', '18:30'),
        ]
        slots2 = [
            ('08:30', '11:40'),
            ('13:00', '13:45'),
            ('14:30', '16:30'),
            ('17:30', '18:30'),
        ]
        bounds = ('09:00', '18:00')
        min_slot = 30  # in minutes

        self.assertEqual(
            find_available_slots(slots1, slots2, bounds, min_slot),
            [
                ('09:00', '09:50'),
                ('10:00', '11:40'),
                ('14:30', '15:30'),
                ('17:30', '18:00'),
            ]
        )


if __name__ == '__main__':
    unittest.main()
