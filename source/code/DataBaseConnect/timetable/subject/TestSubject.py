import unittest
import sqlite3
from Subject import Subject

class TestSubject(unittest.TestCase):
    def setUp(self) -> None:
        db = sqlite3.connect('testDB.db')
        cur = db.cursor()
        self.subject = Subject(cur, db)

    def test_read(self):
        self.assertEqual(self.subject.read(), [(1, 'Fiz.Kult.', 1), (2, 'INO, praktika', 2), (3, 'Fizika, praktika', 3),
                                               (4, 'Istoriya, praktika', 4), (5, 'Vishmat, lektsiya', 5), (6, 'Vishmat, praktika', 5),
                                               (7, 'Fizika, lektsiya', 6), (8, 'VvIT, praktika', 7), (9, 'DevOps, praktika', 8),
                                               (10, 'Istoriya, lektsiya', 4), (11, 'BD, lektsiya', 9), (12, 'BD, praktika', 9),
                                               (13, 'Fizika, lab.', 10)])

    def test_read_by_id(self):
        self.assertEqual(self.subject.read_by_id(1), [(1, 'Fiz.Kult.', 1)])

    def test_read_by_teacher(self):
        self.assertEqual(self.subject.read_by_teacher(10), [(13, 'Fizika, lab.', 10)])

    def test_insert(self):
        self.subject.insert(14, '14 subject', 11)
        self.assertEqual(self.subject.read_by_id(14), [(14, '14 subject', 11)])
        self.subject.delete(14)

    def test_update(self):
        self.subject.update(99, '99 subject', 99, 1)
        self.assertEqual(self.subject.read_by_id(99), [(99, '99 subject', 99)])
        self.subject.update(1, 'Fiz.Kult.', 1, 99)

    def test_delete(self):
        self.subject.insert(99, '99 subject', 99)
        self.subject.delete(99)
        self.assertEqual(self.subject.read_by_id(99), [])

if __name__ == "__main__":
    unittest.main()