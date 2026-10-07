from datetime import date
import unittest
from sprout.reminders import due_plants


class ReminderTests(unittest.TestCase):
    def test_due_today_and_overdue_but_not_future(self):
        plants = [dict(name='Fern', last_watered='2026-10-01'),
                  dict(name='Ivy', last_watered='2026-10-02'),
                  dict(name='Aloe', last_watered='2026-10-03')]
        due = due_plants(plants, date(2026, 10, 8), {'watering_interval_days': 7})
        self.assertEqual([p['name'] for p in due], ['Fern'])
        due = due_plants(plants, date(2026, 10, 9), {'watering_interval_days': 7})
        self.assertEqual([p['name'] for p in due], ['Fern', 'Ivy'])
