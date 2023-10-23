class Teachers:

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def read(self):
        self.cursor.execute(f"SELECT id, surname, name, id_department FROM teachers ORDER BY id;")
        return list(self.cursor.fetchall())

    def read_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM teachers WHERE id={id};")
        return list(self.cursor.fetchall())

    def read_by_depart(self, department_id):
        self.cursor.execute(f"SELECT * FROM teachers WHERE id_department={department_id};")
        return list(self.cursor.fetchall())

    def insert(self, id, surname, name, id_department):
        self.cursor.execute(
            f"INSERT INTO teachers(id,surname,name,id_department)"
            f" VALUES ({id},'{surname}','{name}',{id_department});")
        self.conn.commit()

    def update(self, id, surname, name, id_department, current_id):
        self.cursor.execute(
            f"UPDATE teachers SET id={id}, surname='{surname}', name='{name}' , id_department={id_department}"
            f" WHERE id={current_id};")
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute(f"DELETE FROM teachers WHERE id={id};")
        self.conn.commit()
