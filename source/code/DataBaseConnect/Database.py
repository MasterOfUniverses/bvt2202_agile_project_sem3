from .timetable.Timetable import Timetable
import json
import psycopg2

class Database:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self, connect_options):
        self.conn = psycopg2.connect(**connect_options)
        self.cursor = self.conn.cursor()
        self.timetable = Timetable(self.cursor, self.conn)
