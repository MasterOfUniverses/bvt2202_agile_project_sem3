import os, json
import psycopg2

def db_test():
    entry_data = str(os.path.dirname(os.path.abspath(__file__)))
    entry_data += "/DataBaseConnect/options_for_connect.json"
    entry_data = os.path.normpath(entry_data)
    entry_data = open(entry_data, "r")
    entry_data = json.load(entry_data)

    try:
        connection = psycopg2.connect(**entry_data)
        cursor = connection.cursor()
        # conn_timetable = Timetable(cursor, connection)
        return "Test passed"
    except:
        return "Test failed"
    
print(db_test())