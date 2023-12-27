import unittest
import sqlite3
from Teachers import Teachers

class TestSubject(unittest.TestCase):
    def setUp(self) -> None:
        db = sqlite3.connect('testDB.db')
        cur = db.cursor()
        self.teachers = Teachers(cur, db)

    def test_read(self):
        self.assertEqual(self.teachers.read(), [(1, 'Koroleva', 'Svetlana Anatolievna', 1), (2, 'Voronova', 'E.V.', 2),
                                                (3, 'Faizulaev', 'Vladimir Nurullaevich', 3), (4, 'Sklyar', 'Lidiya Nikolaevna', 4),
                                                (5, 'Shaimardanova', 'Liliya Kimmatovna', 5), (6, 'Valkovskiy', 'Sergey Nikolaevich', 3),
                                                (7, 'Furletov', 'Yuriy Mikhailovich', 3), (8, 'Timchuk', 'Andrey Vasilievich', 7),
                                                (9, 'Polishyuk', 'Yuriy Vladimirovich', 6), (10, 'Trenin', 'Andrey Evgenievich', 3)])

    def test_read_by_id(self):
        self.assertEqual(self.teachers.read_by_id(1), [(1, 'Koroleva', 'Svetlana Anatolievna', 1)])

    def test_read_by_teacher(self):
        self.assertEqual(self.teachers.read_by_depart(5), [(5, 'Shaimardanova', 'Liliya Kimmatovna', 5)])

    def test_insert(self):
        self.teachers.insert(11, '11 surname', '11 name', 11)
        self.assertEqual(self.teachers.read_by_id(11), [(11, '11 surname', '11 name', 11)])
        self.teachers.delete(11)

    def test_update(self):
        self.teachers.update(99, '99 surname', '99 name', 99, 1)
        self.assertEqual(self.teachers.read_by_id(99), [(99, '99 surname', '99 name', 99)])
        self.teachers.update(1, 'Koroleva', 'Svetlana Anatolievna', 1, 99)

    def test_delete(self):
        self.teachers.insert(99, '99 surname', '99 name', 99)
        self.teachers.delete(99)
        self.assertEqual(self.teachers.read_by_id(99), [])

if __name__ == "__main__":
    unittest.main()