class Departments:

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def read(self):
        self.cursor.execute(f"SELECT id, link, room_numb FROM departments ORDER BY id;")
        return list(self.cursor.fetchall())

    def read_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM departments WHERE id={id};")
        return list(self.cursor.fetchall())

    def insert(self, id, link, room_numb):
        self.cursor.execute(f"INSERT INTO departments(id,link,room_numb) VALUES ({id},'{link}','{room_numb}');")
        self.conn.commit()

    def update(self, id, link, room_numb, current_id):
        self.cursor.execute(
            f"UPDATE departments SET id={id}, link='{link}', room_numb='{room_numb}' WHERE id={current_id};")
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute(f"DELETE FROM departments WHERE id={id};")
        self.conn.commit()
