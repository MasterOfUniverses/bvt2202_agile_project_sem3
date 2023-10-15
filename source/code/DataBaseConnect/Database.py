from timetable.Timetable import Timetable
import json
import psycopg2

class Database:

    def __init__(self, connect_options):
        self.conn = psycopg2.connect(**connect_options)
        self.cursor = self.conn.cursor()
        self.timetable = Timetable(self.cursor, self.conn)
