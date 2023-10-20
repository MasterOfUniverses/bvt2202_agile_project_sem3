from PyQt5.QtWidgets import QPushButton, QTableWidgetItem, QMessageBox


class Teachers:

    def __init__(self, database, table):
        self.dataBase = database
        self.table = table
        self.update_teachers()

    def update_teachers(self):
        records = self.dataBase.timetable.teachers.read()

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
            update_button.clicked.connect(self._return_lambda_teachers_update(i, r[0]))
            self.table.setCellWidget(i, 5, delete_button)
            delete_button.clicked.connect(self._return_lambda_teachers_delete(i, r[0]))
            i = i + 1
        i = 0
        insert_button = QPushButton("Add")
        self.table.setItem(len(records), 0, QTableWidgetItem(""))
        self.table.setItem(len(records), 1, QTableWidgetItem(""))
        self.table.setItem(len(records), 2, QTableWidgetItem(""))
        self.table.setItem(len(records), 3, QTableWidgetItem(""))
        self.table.setItem(len(records), 5, QTableWidgetItem(None))
        self.table.setCellWidget(len(records), 4, insert_button)
        insert_button.clicked.connect(self._return_lambda_teachers_insert(len(records)))
        self.table.resizeRowsToContents()

    def _change_teachers(self, row_num, id_code):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count * int(not (len(records) == 1 and int(row[0]) != id_code))
        id_dep_value = 0
        if str(row[3]) == 'None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[3])
            records = self.dataBase.timetable.departments.read_by_id(id_dep_value)
            count = count * int(len(records) == 1)
        records = self.dataBase.timetable.subject.read_by_teacher(int(id_code))
        count = count * int(len(records) == 0 or int(row[0]) == id_code)
        if count > 0:
            try:
                self.dataBase.timetable.teachers.update(int(row[0]), row[1], row[2], id_dep_value, int(id_code))
            except:
                QMessageBox.about(self.table, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Update: Exists such id")
        self.table.resizeRowsToContents()
        self.update_teachers()

    def _insert_teachers(self, row_num):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.teachers.read_by_id(int(row[0]))
        count = count * int(len(records) == 0)
        id_dep_value = 0
        if str(row[3]) == 'None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[3])
            records = self.dataBase.timetable.departments.read_by_id(id_dep_value)
            count = count * int(len(records) == 1)
        if count > 0:
            try:
                self.dataBase.timetable.teachers.insert((row[0]), row[1], row[2], id_dep_value)
            except:
                QMessageBox.about(self.table, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Add: Exists such id")
        self.table.resizeRowsToContents()
        self.update_teachers()

    def _delete_teachers(self, row_num, id_code):
        count = 0
        records = self.dataBase.timetable.subject.read_by_teacher(int(id_code))
        count = count + len(records)
        if count == 0:
            try:
                self.dataBase.timetable.teachers.delete(int(id_code))
            except:
                QMessageBox.about(self.table, "Error", "Delete: error")
        else:
            QMessageBox.about(self.table, "Error", "Delete: can't delete: there are foreign keys in subjects")
        self.table.resizeRowsToContents()
        self.update_teachers()

    def _return_lambda_teachers_insert(self, r):
        return lambda: self._insert_teachers(r)

    def _return_lambda_teachers_update(self, i, id_code):
        return lambda: self._change_teachers(i, id_code)

    def _return_lambda_teachers_delete(self, i, id_code):
        return lambda: self._delete_teachers(i, id_code)
