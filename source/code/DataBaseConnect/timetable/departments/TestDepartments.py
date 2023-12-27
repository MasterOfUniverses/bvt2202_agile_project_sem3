import unittest
import sqlite3
from Departments import Departments

class TestDepartments(unittest.TestCase):
    def setUp(self) -> None:
        db = sqlite3.connect('testDB.db')
        cur = db.cursor()
        self.departments = Departments(cur, db)

    def test_read(self):
        self.assertEqual(self.departments.read(), [(1, 'Fiz.Kult Kafedra', '301'), (2, 'INO Kafedra', '302'),
                                                   (3, 'Fizika Kafedra', '303'), (4, 'Istoriya Kafedra', '304'),
                                                   (5, 'Vishmat Kafedra', '305'), (6, 'VvIT Kafedra', '306'),
                                                   (7, 'DevOps Kafedra', '307')])

    def test_read_by_id(self):
        self.assertEqual(self.departments.read_by_id(7), [(7, 'DevOps Kafedra', '307')])

    def test_insert(self):
        self.departments.insert(8, '8 Kafedra', '308')
        self.assertEqual(self.departments.read_by_id(8), [(8, '8 Kafedra', '308')])
        self.departments.delete(8)

    def test_update(self):
        self.departments.update(8, 'DevOps Kafedra', '307', 7)
        self.assertEqual(self.departments.read_by_id(8), [(8, 'DevOps Kafedra', '307')])
        self.departments.update(7, 'DevOps Kafedra', '307', 8)

    def test_delete(self):
        self.departments.insert(8, '8 Kafedra', '308')
        self.departments.delete(8)
        self.assertEqual(self.departments.read_by_id(8), [])

if __name__ == "__main__":
    unittest.main()