sql1 = "INSERT INTO times(id, start_time, end_time) VALUES (1, '09:30','11:05');\
    INSERT INTO times(id, start_time, end_time) VALUES (2, '11:20','12:55');\
    INSERT INTO times(id, start_time, end_time) VALUES (3, '13:10','14:45');\
    INSERT INTO times(id, start_time, end_time) VALUES (4, '15:25','17:00');\
    INSERT INTO times(id, start_time, end_time) VALUES (5, '17:15','18:50');"


sql2 = "INSERT INTO teachers(id, surname, name) VALUES (1,'Королева','Светлана Анатольевна');\
    INSERT INTO teachers(id, surname, name) VALUES (2, 'Воронова','Е.В.');\
    INSERT INTO teachers(id, surname, name) VALUES (3, 'Файзулаев','Владимир Нуруллаевич');\
    INSERT INTO teachers(id, surname, name) VALUES (4, 'Скляр','Лидия Николаевна');\
    INSERT INTO teachers(id, surname, name) VALUES (5, 'Шаймарданова','Лилия Кимматовна');\
    INSERT INTO teachers(id, surname, name) VALUES (6, 'Вальковский','Сергей Николаевич');\
    INSERT INTO teachers(id, surname, name) VALUES (7, 'Фурлетов','Юрий Михайлович');\
    INSERT INTO teachers(id, surname, name) VALUES (8, 'Тимчук','Андрей Васильевич');\
    INSERT INTO teachers(id, surname, name) VALUES (9, 'Полищук','Юрий Владимирович');\
    INSERT INTO teachers(id, surname, name) VALUES (10, 'Тренин','Андрей Евгеньевич');"

sql3 = "INSERT INTO subject(id, name) VALUES (1, '<Пусто>');\
    INSERT INTO subject(id, name,id_teacher) VALUES (2, 'Физ.культ.',1);\
    INSERT INTO subject(id, name,id_teacher) VALUES (3, 'ИНО, практика',2);\
    INSERT INTO subject(id, name,id_teacher) VALUES (4, 'Физика, практика',3);\
    INSERT INTO subject(id, name,id_teacher) VALUES (5, 'История, практика',4);\
    INSERT INTO subject(id, name,id_teacher) VALUES (6, 'Вышмат, практика',5);\
    INSERT INTO subject(id, name,id_teacher) VALUES (7, 'Вышмат, лекция',5);\
    INSERT INTO subject(id, name,id_teacher) VALUES (8, 'Физика, лекция',6);\
    INSERT INTO subject(id, name,id_teacher) VALUES (9, 'ВвИТ, практика',7);\
    INSERT INTO subject(id, name,id_teacher) VALUES (10, 'DevOps, практика',8);\
    INSERT INTO subject(id, name,id_teacher) VALUES (11, 'История, лекция',4);\
    INSERT INTO subject(id, name,id_teacher) VALUES (12, 'Базы Данных, лекция',9);\
    INSERT INTO subject(id, name,id_teacher) VALUES (13, 'Базы Данных, практика',9);\
    INSERT INTO subject(id, name,id_teacher) VALUES (14, 'Физика, лаб.',10);"

sql4 = "INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,1,1,2,'Н-С/З');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,1,2,3,'Н-322');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,1,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,1,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,1,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,2,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,2,2,3,'Н-405');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,2,3,4,'Н-332а');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,2,4,5,'Н-318');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,2,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,3,1,6,'Н-301');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,3,2,6,'Н-301');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,3,3,7,'Н-514');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,3,4,8,'Н-226');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,3,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,4,1,9,'А-Л-203');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,4,2,10,'А-ВЦ-206');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,4,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,4,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,4,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,5,1,11,'Н-227');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,5,2,12,'Н-535');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,5,3,2,'Н-С/З');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,5,4,13,'Н-410');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,5,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,6,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,6,2,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,6,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,6,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (False,6,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,1,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,1,2,7,'Н-514');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,1,3,5,'Н-316');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,1,4,14,'Н-340');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,1,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,2,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,2,2,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,2,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,2,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,2,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,3,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,3,2,10,'А-ВЦ-302');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,3,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,3,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,3,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,4,1,9,'А-Л-205');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,4,2,9,'А-Л-205');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,4,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,4,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,4,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,5,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,5,2,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,5,3,2,'Н-С/З');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,5,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,5,5,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,6,1,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,6,2,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,6,3,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,6,4,1,'<пусто>');\
    INSERT INTO timetable(is_even_week, day, id_time, id_subj, room_numb) VALUES (True,6,5,1,'<пусто>');"
