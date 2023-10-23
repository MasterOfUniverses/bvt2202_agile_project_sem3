SET PGPASSWORD=
psql -U postgres -d postgres -h localhost -p 5432 -a -f "db_start_script.sql"
psql -U postgres -d bot_timetable -h localhost -p 5432 -a -f "create_script.sql"
psql -U postgres -d bot_timetable -h localhost -p 5432 -a -f "insert_script.sql"
psql -U postgres -d bot_timetable -h localhost -p 5432 -a -f "insert_script2.sql"