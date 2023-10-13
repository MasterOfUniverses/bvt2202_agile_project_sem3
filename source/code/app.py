import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QLayout, QTabWidget, QVBoxLayout,QWidget
from PyQt5 import QtCore

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        #Конект к БД
        self.conn = psycopg2.connect(
            host="localhost",
            database="bot_timetable",
            user="postgres",
            password="val_2000",
            client_encoding="UTF8"
        )
        self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor()
        
        # Получение всех таблиц
        self.cur.execute("SELECT table_name FROM information_schema.tables where table_schema = 'public';")
        gg = self.cur.fetchall()
        self.table_name = [i[0] for i in gg]

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        
        #Создания tab для всех таблиц
        for name in self.table_name:
            self.cur.execute(f"SELECT * FROM {name}")
            rows = self.cur.fetchall()
            table = QTableWidget()
            self.table_update(table,rows)
            self.tab_widget.addTab(table, name)

    
        layout.addWidget(self.tab_widget)

        #Создание одной кнопки обновить
        self.update_button = QPushButton("Обновить", self)
        self.update_button.clicked.connect(self.update_tables)
        layout.addWidget(self.update_button)
        
        self.setLayout(layout)

        table = self.tab_widget.widget(0)
        row_count = table.rowCount()
        #col_count = table.colounCount()

    #При нажатии кнопки обновить
    def update_tables(self):
        for i in range(len(self.table_name)-2):
            table = self.tab_widget.widget(i)
            row = table.rowCount()
            col = table.columnCount()
            for row in range(row-1):
                values = []
                print(row)
                for col in range(col-2):
                    print(col)
                    cell_value = table.item(row, col).text()
                    print(cell_value)
                    values.append(cell_value)
                # выполнение SQL-запроса на изменение значений в базе данных
                #print(values[0])
                if values:
                    sql_query = f" UPDATE {self.table_name[i]} SET name='{values[0]}' where name = '{values[0]}';"
                    self.cur.execute(sql_query)
            self.conn.commit()
            self.cur.execute(f"SELECT * FROM {self.table_name[i]}")
            rows = self.cur.fetchall()
            self.table_update(table,rows)

    #Создание tab для таблиц
    def table_update(self,table, rows):
        table.setRowCount(len(rows))
        if(len(rows) == 0):
            table.setColumnCount(2)
        else:
            table.setColumnCount(len(rows[0])+2)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                table.setItem(i, j, item)
            button1 = QPushButton("Изменить",table)
            button2 = QPushButton("Удалить", table)
            button1.clicked.connect(self.edit_button_clicked)
            button2.clicked.connect(self.delete_button_clicked)
            table.setCellWidget(i, len(row), button1)
            table.setCellWidget(i, len(row)+1, button2)

    #Кнопка изменить
    def edit_button_clicked(self):
        button = self.sender()
        table_widget = button.parent().parent()
        index = table_widget.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            col = index.column()
            print(f"нажата кнопка 'Изменить' в строке {row}, колонке {col}")
            for i in range(table_widget.columnCount()-2):
                item = table_widget.item(row, i)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                table_widget.editItem(item)
            table_widget.viewport().update()

    #Кнопка удалить
    def delete_button_clicked(self):
        button = self.sender()
        table = button.parent().parent()
        row = button.row()
        col = button.column()
        index = table.model().index(row, col)
        if index.isValid():
            print(f"нажата кнопка 'Удалить' в строке {row}, колонке {col}")
            table.removeRow(row)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())