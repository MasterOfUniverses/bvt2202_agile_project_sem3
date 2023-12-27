CREATE TABLE times(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, start_time time NOT NULL, end_time time NOT NULL);
INSERT INTO times(start_time, end_time) VALUES ('09:30','11:05');
INSERT INTO times(start_time, end_time) VALUES ('11:20','12:55');
INSERT INTO times(start_time, end_time) VALUES ('13:10','14:45');
INSERT INTO times(start_time, end_time) VALUES ('15:25','17:00');
INSERT INTO times(start_time, end_time) VALUES ('17:15','18:50');
CREATE TABLE departments(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, link VARCHAR NOT NULL, room_numb VARCHAR NOT NULL);
CREATE TABLE teachers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, surname VARCHAR NOT NULL, name VARCHAR NOT NULL, id_department INTEGER, FOREIGN KEY (id_department) REFERENCES departments(id));
CREATE TABLE subject(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR NOT NULL UNIQUE, id_teacher INTEGER, FOREIGN KEY (id_teacher) REFERENCES teachers(id));
CREATE TABLE timetable(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,is_even_week BOOLEAN NOT NULL, day INTEGER CHECK (day>0 and day<7) NOT NULL, id_time INTEGER NOT NULL, id_subj INTEGER NOT NULL, room_numb VARCHAR NOT NULL,FOREIGN KEY (id_time) REFERENCES times(id), FOREIGN KEY (id_subj) REFERENCES subject(id));

