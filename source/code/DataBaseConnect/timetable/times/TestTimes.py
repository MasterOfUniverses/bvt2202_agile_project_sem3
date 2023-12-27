import unittest
import sqlite3
from Times import Times

class TestSubject(unittest.TestCase):
    def setUp(self) -> None:
        db = sqlite3.connect('testDB.db')
        cur = db.cursor()
        self.times = Times(cur, db)

    def test_read(self):
        self.assertEqual(self.times.read(), [(1, '09:30', '11:05'), (2, '11:20', '12:55'), (3, '13:10', '14:45'),
                                             (4, '15:25', '17:00'), (5, '17:15', '18:50')])

    def test_read_by_id(self):
        self.assertEqual(self.times.read_by_id(1), [(1, '09:30', '11:05')])

    def test_insert(self):
        self.times.insert(6, 'all', 'night')
        self.assertEqual(self.times.read_by_id(6), [(6, 'all', 'night')])
        self.times.delete(6)

    def test_update(self):
        self.times.update(99, 'all', 'night', 1)
        self.assertEqual(self.times.read_by_id(99), [(99, 'all', 'night')])
        self.times.update(1, '09:30', '11:05', 99)

    def test_delete(self):
        self.times.insert(99, 'all', 'night')
        self.times.delete(99)
        self.assertEqual(self.times.read_by_id(99), [])

if __name__ == "__main__":
    unittest.main()