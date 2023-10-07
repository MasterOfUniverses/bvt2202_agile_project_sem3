import psycopg2


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(database="bot_timetable",
                                     user="admin_tt",
                                     password="admin_lab78",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()

    # timetable

    def take_day_timetable(self, week, day):
        self.cursor.execute(
            f"SELECT id_time,id_subj,room_numb,id FROM timetable "
            f"WHERE day={day + 1} AND is_even_week={week} ORDER BY id_time;")
        return list(self.cursor.fetchall())

    def take_timetable_by_time(self, id_time):
        self.cursor.execute(f"SELECT * FROM timetable WHERE id_time={id_time};")
        return list(self.cursor.fetchall())

    def take_timetable_by_subj(self, subj_id):
        self.cursor.execute(f"SELECT * FROM timetable WHERE id_subj={subj_id};")
        return list(self.cursor.fetchall())

    def insert_day_timetable(self, id, week, day, id_time, id_subj, room_numb):
        self.cursor.execute(
            f"INSERT INTO timetable(id,is_even_week,day,id_time,id_subj,room_numb)"
            f" VALUES ({id},'{week}',{day + 1},{id_time},{id_subj},'{room_numb}');")
        self.conn.commit()

    def update_timetable(self, id_time, id_subj, room_numb, id, current_id):
        self.cursor.execute(
            f"UPDATE timetable SET id_time={id_time}, id_subj={id_subj}, room_numb='{room_numb}', id={id}"
            f" WHERE id={current_id};")
        self.conn.commit()

    def delete_day_timetable(self, id):
        self.cursor.execute(f"DELETE FROM timetable WHERE id={id};")
        self.conn.commit()

    # times

    def take_times_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM times WHERE id={id};")
        return list(self.cursor.fetchall())

    def take_times(self):
        self.cursor.execute(f"SELECT id, start_time, end_time FROM times ORDER BY id;")
        return list(self.cursor.fetchall())

    def insert_times(self, id, start_time, end_time):
        self.cursor.execute(f"INSERT INTO times(id,start_time,end_time) VALUES ({id},'{start_time}','{end_time}');")
        self.conn.commit()

    def update_times(self, id, start_time, end_time, current_id):
        self.cursor.execute(
            f"UPDATE times SET id={id}, start_time='{start_time}', end_time='{end_time}' WHERE id={current_id};")
        self.conn.commit()

    def delete_times(self, id):
        self.cursor.execute(f"DELETE FROM times WHERE id={id};")
        self.conn.commit()

    # teachers

    def take_teachers(self):
        self.cursor.execute(f"SELECT id, surname, name, id_department FROM teachers ORDER BY id;")
        return list(self.cursor.fetchall())

    def take_teachers_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM teachers WHERE id={id};")
        return list(self.cursor.fetchall())

    def take_teachers_by_depart(self, department_id):
        self.cursor.execute(f"SELECT * FROM teachers WHERE id_department={department_id};")
        return list(self.cursor.fetchall())

    def insert_teachers(self, id, surname, name, id_department):
        self.cursor.execute(
            f"INSERT INTO teachers(id,surname,name,id_department)"
            f" VALUES ({id},'{surname}','{name}',{id_department});")
        self.conn.commit()

    def update_teachers(self, id, surname, name, id_department, current_id):
        self.cursor.execute(
            f"UPDATE teachers SET id={id}, surname='{surname}', name='{name}' , id_department={id_department}"
            f" WHERE id={current_id};")
        self.conn.commit()

    def delete_teachers(self, id):
        self.cursor.execute(f"DELETE FROM teachers WHERE id={id};")
        self.conn.commit()

    # departments

    def take_departments(self):
        self.cursor.execute(f"SELECT id, link, room_numb FROM departments ORDER BY id;")
        return list(self.cursor.fetchall())

    def take_departments_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM departments WHERE id={id};")
        return list(self.cursor.fetchall())

    def insert_departments(self, id, link, room_numb):
        self.cursor.execute(f"INSERT INTO departments(id,link,room_numb) VALUES ({id},'{link}','{room_numb}');")
        self.conn.commit()

    def update_departments(self, id, link, room_numb, current_id):
        self.cursor.execute(
            f"UPDATE departments SET id={id}, link='{link}', room_numb='{room_numb}' WHERE id={current_id};")
        self.conn.commit()

    def delete_departments(self, id):
        self.cursor.execute(f"DELETE FROM departments WHERE id={id};")
        self.conn.commit()

    # subjects

    def take_subjects(self):
        self.cursor.execute(f"SELECT id, name, id_teacher FROM subject ORDER BY id;")
        return list(self.cursor.fetchall())

    def take_subjects_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM subject WHERE id={id};")
        return list(self.cursor.fetchall())

    def take_subject_by_teacher(self, teacher_id):
        self.cursor.execute(f"SELECT * FROM subject WHERE id_teacher={teacher_id};")
        return list(self.cursor.fetchall())

    def insert_subjects(self, id, name, id_teacher):
        self.cursor.execute(
            f"INSERT INTO subject(id,name,id_teacher) VALUES ({id},'{name}',{id_teacher});")
        self.conn.commit()

    def update_subjects(self, id, name, id_teacher, current_id):
        self.cursor.execute(
            f"UPDATE subject SET id={id}, name='{name}' , id_teacher={id_teacher} WHERE id={current_id};")
        self.conn.commit()

    def delete_subjects(self, id):
        self.cursor.execute(f"DELETE FROM subject WHERE id={int(id_code)};")
        self.conn.commit()

