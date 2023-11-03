psql -U postgres -W admin_lab78 -d postgres -h localhost -p 5432 -a -f "db_start_script.sql"
psql -U postgres -W admin_lab78 -d bot_timetable -h localhost -p 5432 -a -f "create_script.sql"
psql -U postgres -W admin_lab78 -d bot_timetable -h localhost -p 5432 -a -f "insert_script.sql"
psql -U postgres -W admin_lab78 -d bot_timetable -h localhost -p 5432 -a -f "insert_script2.sql"
