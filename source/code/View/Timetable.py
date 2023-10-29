from PyQt5.QtWidgets import QPushButton, QTableWidgetItem, QMessageBox
from .utils import week_to_type_bool


class Timetable:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timetable, cls).__new__(cls)
        return cls.instance

    def __init__(self, database, table, week, day):
        self.dataBase = database
        self.table = table
        self.week = week
        self.day = day
        self.update_tt_day_table()

    def update_tt_day_table(self):

        records = self.dataBase.timetable.read(week_to_type_bool(self.week), self.day)

        self.table.setRowCount(len(records) + 1)
        i = 0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.table.setCellWidget(i, 4, update_button)
            update_button.clicked.connect(self._return_lambda_tt_update(i, r[3]))
            self.table.setCellWidget(i, 5, delete_button)
            delete_button.clicked.connect(self._return_lambda_tt_delete(i, r[3]))
            i = i + 1
        i = 0
        insert_button = QPushButton("Add")
        self.table.setItem(len(records), 0, QTableWidgetItem(""))
        self.table.setItem(len(records), 1, QTableWidgetItem(""))
        self.table.setItem(len(records), 2, QTableWidgetItem(""))
        self.table.setItem(len(records), 3, QTableWidgetItem(""))
        self.table.setItem(len(records), 5, QTableWidgetItem(None))
        self.table.setCellWidget(len(records), 4, insert_button)
        insert_button.clicked.connect(self._return_lambda_tt_insert(len(records)))
        self.table.resizeRowsToContents()

    def _change_tt_day(self, row_num, id_code):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count * len(records)
        records = self.dataBase.timetable.subject.read_by_id(int(row[1]))
        count = count * len(records)
        records = self.dataBase.timetable.times.read_by_id(int(row[3]))
        count = count * int(not (len(records) == 1 and int(row[3]) != id_code))
        if count > 0:

            try:
                self.dataBase.timetable.update(int(row[0]), int(row[1]), row[2], int(row[3]), int(id_code))
            except:
                QMessageBox.about(self.table, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Update: No such time or subject or Exists such id")
        self.table.resizeRowsToContents()
        self.update_tt_day_table()

    def _insert_tt_day(self, row_num):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        try:
            records = self.dataBase.timetable.times.read_by_id(int(row[0]))
            count = count * len(records)
            records = self.dataBase.timetable.times.read_by_id(int(row[1]))
            count = count * len(records)
            records = self.dataBase.timetable.times.read_by_id(int(row[3]))
            count = count * int(len(records) == 0)
        except:
            count = 0
        if count > 0:
            try:
                self.dataBase.timetable.insert_day(int(row[3]), week_to_type_bool(self.week), self.day, int(row[0]),
                                                   int(row[1]), row[2])
            except:
                QMessageBox.about(self.table, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Add: No such time or subject or Exists such id")
        self.table.resizeRowsToContents()
        self.update_tt_day_table()

    def _delete_tt_day(self, row_num, id_code):
        try:
            self.dataBase.timetable.delete_day(int(id_code))
        except:
            QMessageBox.about(self.table, "Error", "Delete: error")
        self.table.resizeRowsToContents()

        self.update_tt_day_table()

    def _return_lambda_tt_insert(self, r):
        return lambda: self._insert_tt_day(r)

    def _return_lambda_tt_update(self, i, id_code):
        return lambda: self._change_tt_day(i, id_code)

    def _return_lambda_tt_delete(self, i, id_code):
        return lambda: self._delete_tt_day(i, id_code)
