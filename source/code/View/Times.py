from PyQt5.QtWidgets import QPushButton, QTableWidgetItem, QMessageBox


class Times:

    def __init__(self, database, table):
        self.dataBase = database
        self.table = table
        self.update_times()

    def update_times(self):
        records = self.dataBase.timetable.times.read()

        self.table.setRowCount(len(records) + 1)
        i = 0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.table.setCellWidget(i, 3, update_button)
            update_button.clicked.connect(self._return_lambda_times_update(i, r[0]))
            self.table.setCellWidget(i, 4, delete_button)
            delete_button.clicked.connect(self._return_lambda_times_delete(i, r[0]))
            i = i + 1
        i = 0
        insert_button = QPushButton("Add")
        self.table.setItem(len(records), 0, QTableWidgetItem(""))
        self.table.setItem(len(records), 1, QTableWidgetItem(""))
        self.table.setItem(len(records), 2, QTableWidgetItem(""))
        self.table.setItem(len(records), 4, QTableWidgetItem(None))
        self.table.setCellWidget(len(records), 3, insert_button)
        insert_button.clicked.connect(self._return_lambda_times_insert(len(records)))
        self.table.resizeRowsToContents()

    def _change_times(self, row_num, id_code):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count * int(not (len(records) == 1 and int(row[0]) != id_code))
        records = self.dataBase.timetable.times.read_by_id(int(id_code))
        count = count * int(len(records) == 0 or int(row[0]) == id_code)
        if count > 0:

            try:
                self.dataBase.timetable.times.update(int(row[0]), row[1], row[2], int(id_code))
            except:
                QMessageBox.about(self.table, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Update: Exists such id")
        self.table.resizeRowsToContents()
        self.update_times()

    def _insert_times(self, row_num):
        row = list()
        for col in range(self.table.columnCount() - 2):
            try:
                row.append(self.table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count * int(len(records) == 0)
        if count > 0:
            try:
                self.dataBase.timetable.times.insert(int(row[0]), row[1], row[2])
            except:
                QMessageBox.about(self.table, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self.table, "Error", "Add: Exists such id")
        self.table.resizeRowsToContents()
        self.update_times()

    def _delete_times(self, row_num, id_code):
        count = 0
        records = self.dataBase.timetable.read_by_time(int(id_code))
        count = count + len(records)
        if count == 0:
            try:
                self.dataBase.timetable.times.delete(int(id_code))
            except:
                QMessageBox.about(self.table, "Error", "Delete: error")
        else:
            QMessageBox.about(self.table, "Error", "Delete: can't delete: there are foreign keys in timetable")
        self.table.resizeRowsToContents()
        self.update_times()

    def _return_lambda_times_insert(self, r):
        return lambda: self._insert_times(r)

    def _return_lambda_times_update(self, i, id_code):
        return lambda: self._change_times(i, id_code)

    def _return_lambda_times_delete(self, i, id_code):
        return lambda: self._delete_times(i, id_code)

