class Subject:

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def read(self):
        self.cursor.execute(f"SELECT id, name, id_teacher FROM subject ORDER BY id;")
        return list(self.cursor.fetchall())

    def read_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM subject WHERE id={id};")
        return list(self.cursor.fetchall())

    def read_by_teacher(self, teacher_id):
        self.cursor.execute(f"SELECT * FROM subject WHERE id_teacher={teacher_id};")
        return list(self.cursor.fetchall())

    def insert(self, id, name, id_teacher):
        self.cursor.execute(
            f"INSERT INTO subject(id,name,id_teacher) VALUES ({id},'{name}',{id_teacher});")
        self.conn.commit()

    def update(self, id, name, id_teacher, current_id):
        self.cursor.execute(
            f"UPDATE subject SET id={id}, name='{name}' , id_teacher={id_teacher} WHERE id={current_id};")
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute(f"DELETE FROM subject WHERE id={id};")
        self.conn.commit()
