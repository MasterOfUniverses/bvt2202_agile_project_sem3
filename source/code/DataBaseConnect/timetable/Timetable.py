from .times.Times import Times
from .departments.Departments import Departments
from .teachers.Teachers import Teachers
from .subject.Subject import Subject


class Timetable:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timetable, cls).__new__(cls)
        return cls.instance

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

        self.times = Times(cursor, conn)
        self.departments = Departments(cursor, conn)
        self.teachers = Teachers(cursor, conn)
        self.subject = Subject(cursor, conn)

    def read(self, week, day):
        self.cursor.execute(
            f"SELECT id_time,id_subj,room_numb,id FROM timetable "
            f"WHERE day={day + 1} AND is_even_week={week} ORDER BY id_time;")
        return list(self.cursor.fetchall())

    def read_by_time(self, id_time):
        self.cursor.execute(f"SELECT * FROM timetable WHERE id_time={id_time};")
        return list(self.cursor.fetchall())

    def read_by_subject(self, subj_id):
        self.cursor.execute(f"SELECT * FROM timetable WHERE id_subj={subj_id};")
        return list(self.cursor.fetchall())

    def insert_day(self, id, week, day, id_time, id_subj, room_numb):
        self.cursor.execute(
            f"INSERT INTO timetable(id,is_even_week,day,id_time,id_subj,room_numb)"
            f" VALUES ({id},'{week}',{day + 1},{id_time},{id_subj},'{room_numb}');")
        self.conn.commit()

    def update(self, id_time, id_subj, room_numb, id, current_id):
        self.cursor.execute(
            f"UPDATE timetable SET id_time={id_time}, id_subj={id_subj}, room_numb='{room_numb}', id={id}"
            f" WHERE id={current_id};")
        self.conn.commit()

    def delete_day(self, id):
        self.cursor.execute(f"DELETE FROM timetable WHERE id={id};")
        self.conn.commit()
