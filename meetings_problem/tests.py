#!/usr/bin/env python3

import unittest

from meeting import find_available_slots


class FindAvailableSlotsTests(unittest.TestCase):

    def test_available_slots_are_found(self):
        """Test the happy path"""
        calendar1 = [
            ('10:00', '10:40'),
            ('12:00', '12:30'),
            ('14:00', '15:30'),
        ]
        calendar2 = [
            ('11:20', '11:50'),
            ('12:00', '12:45'),
            ('14:30', '16:30'),
        ]
        bounds = ('9:00', '18:00')
        min_slot = 30  # in minutes

        self.assertEquals(
            find_available_slots(calendar1, calendar2, bounds, min_slot),
            [
                ('09:00', '10:00'),
                ('10:40', '11:20'),
                ('12:45', '14:00'),
                ('16:30', '18:00'),
            ]
        )


if __name__ == '__main__':
    unittest.main()
