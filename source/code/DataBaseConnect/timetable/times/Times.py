class Times:

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def read_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM times WHERE id={id};")
        return list(self.cursor.fetchall())

    def read(self):
        self.cursor.execute(f"SELECT id, start_time, end_time FROM times ORDER BY id;")
        return list(self.cursor.fetchall())

    def insert(self, id, start_time, end_time):
        self.cursor.execute(f"INSERT INTO times(id,start_time,end_time) VALUES ({id},'{start_time}','{end_time}');")
        self.conn.commit()

    def update(self, id, start_time, end_time, current_id):
        self.cursor.execute(
            f"UPDATE times SET id={id}, start_time='{start_time}', end_time='{end_time}' WHERE id={current_id};")
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute(f"DELETE FROM times WHERE id={id};")
        self.conn.commit()

