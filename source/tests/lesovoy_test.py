import os, json
import psycopg2
from lesovoy_test_hard_reset_data import sql1, sql2, sql3, sql4


# здесь содержится последовательность тестов для проверки работы БД и приложения
# а также методы вывода информации и функция для восстановления БД к исходному состоянию

# функция возврата к исходному состоянию может иметь ценность сам по себе
# либо при некотором преобразовании его можно использовать для создания/заполнения данными БД на компьютере разработчика

def tests_sequence(print_res : bool = False): #print_res отвечает за вывод данных из БД

    # Тест 1 - подключение к БД
    print("Test 1 : connecting to DB ...")
    try:
        # взято из app.py
        # получаем путь к текущему файлу в формате строки
        entry_data = str(os.path.dirname(os.path.abspath(__file__)))
        # получаем параметры для подключения
        entry_data += "\..\code\DataBaseConnect\options_for_connect.json"
        entry_data = open(entry_data, "r")
        # переводим в нужный формат, загружаем в psycopg2.connect, создаём cursor для будущих тестов
        entry_data = json.load(entry_data)
        conn = psycopg2.connect(**entry_data)
        cursor = conn.cursor()
        print('Test 1 passed')

    except Exception as e:
        print('Test 1 failed:', e)
        hard_reset()
        return

    # Тест 2 - вывод данных Departments и teachers в консоль
    print("Test 2 : printing data ...")
    try:
        query = "SELECT * FROM public.teachers ORDER BY id ASC"
        cursor.execute(query)
        data = get_result(cursor.fetchall(),4)
        if(print_res):
            advanced_print(data)
        
        query = "SELECT * FROM public.departments ORDER BY id ASC"
        cursor.execute(query)
        data = get_result(cursor.fetchall(),3)
        if(print_res):
            advanced_print(data)
        print('Test 2 passed')
    except Exception as e:
        print('Test 2 failed:', e)
        hard_reset()
        return

    # Тест 3 - добавление данных в departments и изменение teachers
    print("Test 3 : editing tables ...")
    try:
        query = """
            INSERT INTO departments(id, link, room_numb) VALUES (1,'https://mtuci.ru/about_the_university/structure/573/', 'none');
            INSERT INTO departments(id, link, room_numb) VALUES (2,'https://mtuci.ru/about_the_university/structure/6352/', 'none');
            INSERT INTO departments(id, link, room_numb) VALUES (3,'https://mtuci.ru/about_the_university/structure/574/', 'none');
            INSERT INTO departments(id, link, room_numb) VALUES (4,'https://mtuci.ru/about_the_university/structure/161/?lang=en&ysclid=lqognysc5f633440382', 'none');
        """
        cursor.execute(query)

        query = """
            UPDATE public.teachers SET id_department = 1 WHERE id IN (6,3,10);
            UPDATE public.teachers SET id_department = 2 WHERE id IN (9);
            UPDATE public.teachers SET id_department = 3 WHERE id IN (1);
            UPDATE public.teachers SET id_department = 4 WHERE id IN (5);
        """

        cursor.execute(query)

        print('Test 3 passed')
    except Exception as e:
        print('Test 3 failed:', e)
        hard_reset()
        return  

    # Тест 4 - вывод изменённых данных в консоль
    print("Test 4 : printing edited data ...")
    try:
        query = "SELECT * FROM public.teachers ORDER BY id ASC"
        cursor.execute(query)
        data = get_result(cursor.fetchall(),4)
        if(print_res):
            advanced_print(data)
        query = "SELECT * FROM public.departments ORDER BY id ASC"
        cursor.execute(query)
        data = get_result(cursor.fetchall(),3)
        if(print_res):
            advanced_print(data)
        print('Test 4 passed')
    except Exception as e:
        print('Test 4 failed:', e)
        hard_reset()
        return  

    # Тест 5 - отмена введённых изменений = проверка функции hard_reset
    print("Test 5 : resetting DB ...")
    try:
        hard_reset()
        print('Test 5 passed')
    except Exception as e:
        print('Test 5 failed:', e)
        return

    # Тест 6 - запуск программы
    print("Test 6 : launching app ...")
    try:
        print('Test 6 passed')
    except Exception as e:
        print('Test 6 failed:', e)
        hard_reset()
        return

    # Тест 7 - завершение работы программы
    print("Test 7 : closing app ...")
    try:
        print('Test 7 passed')
    except Exception as e:
        print('Test 7 failed:', e)
        hard_reset()
        return





def get_result(result, columns):
    data = []
    match columns:
        case 3:
            for row in result:
                data.append({
                    'id': row[0],
                    'link': row[1],
                    'room_numb': row[2]
                })

        case 4:
            for row in result:
                data.append({
                    'id': row[0],
                    'surname': row[1],
                    'name': row[2],
                    'id_department': row[3]
                })
    return data

def advanced_print(arr):
    for row in arr:
        print(row)

def hard_reset():
    try:
        entry_data = str(os.path.dirname(os.path.abspath(__file__)))
        entry_data += "\..\code\DataBaseConnect\options_for_connect.json"
        entry_data = open(entry_data, "r")
        entry_data = json.load(entry_data)
        conn = psycopg2.connect(**entry_data)
        cursor = conn.cursor()
        query = 'DELETE FROM public.timetable'
        cursor.execute(query)
        query = 'DELETE FROM public.times'
        cursor.execute(query)
        query = 'DELETE FROM public.subject'
        cursor.execute(query)
        
        query  ="UPDATE public.teachers SET id_department = NULL;"
        cursor.execute(query)

        query = 'DELETE FROM public.teachers'
        cursor.execute(query)
        query = 'DELETE FROM public.departments'
        cursor.execute(query)

        query = sql1
        cursor.execute(query)

        query = sql2
        cursor.execute(query)

        query = sql3
        cursor.execute(query)

        query = sql4
        cursor.execute(query)
        
    
    except Exception as e:
        print("\nHARD RESET FAILED! Please reset database to its original state manually\n")
        print(e)


tests_sequence(True)
# tests_sequence()