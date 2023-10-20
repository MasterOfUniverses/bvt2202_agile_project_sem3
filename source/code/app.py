import sys, json, os
from pathlib import Path
from DataBaseConnect.Database import Database

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                         QTableWidgetItem, QPushButton, QMessageBox)

DAYS_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
WEEKS_NUMBER = 2 #WARNING! db has only two weeks as bool field
                    #for over tt_db - you must change _week_to_type_bool too
DAYS_NUMBER = len(DAYS_NAMES)

class MainWindow(QWidget):
    global DAYS_NAMES, WEEKS_NUMBER, DAYS_NUMBER

    def __init__(self):
        super(MainWindow, self).__init__()
        
        entry_data = str(os.path.dirname(os.path.abspath(__file__))) 
        entry_data += "/DataBaseConnect/options_for_connect.json"
        entry_data = os.path.normpath(entry_data)
        
        entry_data = open(entry_data, "r")
        entry_data = json.load(entry_data)
        self.dataBase = Database(entry_data)

        self.setWindowTitle("bot_timetable")
        self.vbox = QVBoxLayout(self)

        self._create_all_objects()

        for week in range(0,WEEKS_NUMBER):
            self._create_tt_week_tab(week)
        self._create_times_tab()
        self._create_subj_tab()
        self._create_teachers_tab()
        self._create_dep_tab()

    def _week_to_type_bool(self,week): #change if db has another week field then boolean
        if week == 1:
            return "TRUE"
        elif week == 0:
            return "FALSE"
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setInformativeText("no such week in this db")
            self.msg.setText("Error")
            self.msg.setWindowTitle("Error")

    def _create_tt_week_tab(self,week):
        for day in range(0,DAYS_NUMBER):
            self.tt_weeks_day_tabs[week].addTab(self.tt_day_tabs[week][day],DAYS_NAMES[day])   
     
        self.tt_week_svbox[week].addLayout(self.tt_week_shbox_tabs[week])
        self.tt_week_svbox[week].addLayout(self.tt_week_shbox_update[week])
        self.tt_week_shbox_tabs[week].addWidget(self.tt_weeks_day_tabs[week])
        self.tt_week_shbox_update[week].addWidget(self.tt_update_buttons[week])
        self.tt_update_buttons[week].clicked.connect(self._update_tt)

        for day in range(0,DAYS_NUMBER):
            self._create_day_tab(week,day)


    def _create_day_tab(self, week, day):
        self.tt_day_table[week][day].setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tt_day_table[week][day].setColumnCount(len(self.HEADER_NAMES_TT))
        self.tt_day_table[week][day].setHorizontalHeaderLabels(self.HEADER_NAMES_TT)

        self._update_tt_day_table(week, day)

        self.tt_day_mvbox[week][day].addWidget(self.tt_day_table[week][day])
        self.tt_day_gboxes[week][day].setLayout(self.tt_day_mvbox[week][day])

    def _update_tt_day_table(self,week,day):

        records = self.dataBase.timetable.read(self._week_to_type_bool(week), day)

        self.tt_day_table[week][day].setRowCount(len(records) + 1)
        i = 0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.tt_day_table[week][day].setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.tt_day_table[week][day].setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.tt_day_table[week][day].setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.tt_day_table[week][day].setItem(i, 3,QTableWidgetItem(str(r[3])))
            self.tt_day_table[week][day].setCellWidget(i, 4, update_button)
            update_button.clicked.connect(self._return_lambda_tt_update(i,week,day,r[3]))
            self.tt_day_table[week][day].setCellWidget(i, 5, delete_button)
            delete_button.clicked.connect(self._return_lambda_tt_delete(i,week,day,r[3]))
            i=i+1
        i=0
        insert_button = QPushButton("Add")
        self.tt_day_table[week][day].setItem(len(records), 0,QTableWidgetItem(""))
        self.tt_day_table[week][day].setItem(len(records), 1,QTableWidgetItem(""))
        self.tt_day_table[week][day].setItem(len(records), 2,QTableWidgetItem(""))
        self.tt_day_table[week][day].setItem(len(records), 3,QTableWidgetItem(""))
        self.tt_day_table[week][day].setItem(len(records), 5,QTableWidgetItem(None))
        self.tt_day_table[week][day].setCellWidget(len(records),4,insert_button)
        insert_button.clicked.connect(self._return_lambda_tt_insert(len(records),week,day))
        self.tt_day_table[week][day].resizeRowsToContents()

    def _return_lambda_tt_update(self,i,w,d,id_code):
        return lambda: self._change_tt_day(i,w,d,id_code)
    def _return_lambda_tt_delete(self,i,w,d,id_code):
        return lambda: self._delete_tt_day(i,w,d,id_code)
    def _return_lambda_tt_insert(self,r,w,d):
        return lambda: self._insert_tt_day(r,w,d)


    def _change_tt_day(self, row_num, week, day,id_code):
        row = list()
        for col in range(self.tt_day_table[week][day].columnCount()-2):
            try:
                row.append(self.tt_day_table[week][day].item(row_num, col).text())
            except:
                row.append(None)
        count=1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count=count*len(records)
        records = self.dataBase.timetable.subject.read_by_id(int(row[1]))
        count=count*len(records)
        records = self.dataBase.timetable.times.read_by_id(int(row[3]))
        count=count*int(not(len(records)==1 and int(row[3])!=id_code))
        if count>0:

            try:
                self.dataBase.timetable.update(int(row[0]), int(row[1]), row[2], int(row[3]), int(id_code))
            except:
                QMessageBox.about(self, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Update: No such time or subject or Exists such id")
        self.tt_day_table[week][day].resizeRowsToContents()
        self._update_tt_day_table(week,day)

    def _insert_tt_day(self, row_num,week,day):
        row = list()
        for col in range(self.tt_day_table[week][day].columnCount()-2):
            try:
                row.append(self.tt_day_table[week][day].item(row_num, col).text())
            except:
                row.append(None)
        count=1
        try:
            records = self.dataBase.timetable.times.read_by_id(int(row[0]))
            count = count*len(records)
            records = self.dataBase.timetable.times.read_by_id(int(row[1]))
            count = count*len(records)
            records = self.dataBase.timetable.times.read_by_id(int(row[3]))
            count = count*int(len(records) == 0)
        except:
            count = 0
        if count > 0:
            try:
                self.dataBase.timetable.insert_day(int(row[3]), self._week_to_type_bool(week), day, int(row[0]), int(row[1]), row[2])
            except:
                QMessageBox.about(self, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Add: No such time or subject or Exists such id")
        self.tt_day_table[week][day].resizeRowsToContents()
        self._update_tt_day_table(week,day)

    def _delete_tt_day(self,row_num, week, day,id_code):
        try:
            self.dataBase.timetable.delete_day(int(id_code))
        except:
            QMessageBox.about(self, "Error", "Delete: error")
        self.tt_day_table[week][day].resizeRowsToContents()

        self._update_tt_day_table(week,day)

    def _create_times_tab(self):
        self.times_svbox = QVBoxLayout(self.times_tab)
        self.times_shbox_table = QHBoxLayout()
        self.times_shbox_update = QHBoxLayout()
        self.times_svbox.addLayout(self.times_shbox_table)
        self.times_svbox.addLayout(self.times_shbox_update)
        self.times_gbox = QGroupBox("Times")
        self.times_shbox_table.addWidget(self.times_gbox)
        self._create_times_table()
        self.update_times_button = QPushButton("Update")
        self.times_shbox_update.addWidget(self.update_times_button)
        self.update_times_button.clicked.connect(self._update_times)


    def _create_times_table(self):
        self.times_interval_table = QTableWidget()
        self.times_interval_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.times_interval_table.setColumnCount(len(self.HEADER_NAMES_TIMES))
        self.times_interval_table.setHorizontalHeaderLabels(self.HEADER_NAMES_TIMES)
        self.times_mvbox = QVBoxLayout()
        self._update_times()
        self.times_mvbox.addWidget(self.times_interval_table)
        self.times_gbox.setLayout(self.times_mvbox)

    def _update_times(self):
        records = self.dataBase.timetable.times.read()

        self.times_interval_table.setRowCount(len(records) + 1)
        i=0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.times_interval_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.times_interval_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.times_interval_table.setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.times_interval_table.setCellWidget(i, 3, update_button)
            update_button.clicked.connect(self._return_lambda_times_update(i,r[0]))
            self.times_interval_table.setCellWidget(i, 4, delete_button)
            delete_button.clicked.connect(self._return_lambda_times_delete(i,r[0]))
            i=i+1
        i=0
        insert_button = QPushButton("Add")
        self.times_interval_table.setItem(len(records), 0,QTableWidgetItem(""))
        self.times_interval_table.setItem(len(records), 1,QTableWidgetItem(""))
        self.times_interval_table.setItem(len(records), 2,QTableWidgetItem(""))
        self.times_interval_table.setItem(len(records), 4,QTableWidgetItem(None))
        self.times_interval_table.setCellWidget(len(records),3,insert_button)
        insert_button.clicked.connect(self._return_lambda_times_insert(len(records)))
        self.times_interval_table.resizeRowsToContents()
    
    def _return_lambda_times_update(self,i,id_code):
        return lambda: self._change_times(i,id_code)
    def _return_lambda_times_delete(self,i,id_code):
        return lambda: self._delete_times(i,id_code)
    def _return_lambda_times_insert(self,r):
        return lambda: self._insert_times(r)

    def _change_times(self, row_num,id_code):
        row = list()
        for col in range(self.times_interval_table.columnCount()-2):
            try:
                row.append(self.times_interval_table.item(row_num, col).text())
            except:
                row.append(None)    
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count*int(not(len(records) == 1 and int(row[0]) != id_code))
        records = self.dataBase.timetable.times.read_by_id(int(id_code))
        count = count*int(len(records) == 0 or int(row[0]) == id_code)
        if count > 0:

            try:
                self.dataBase.timetable.times.update(int(row[0]), row[1], row[2], int(id_code))
            except:
                QMessageBox.about(self, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Update: Exists such id")
        self.times_interval_table.resizeRowsToContents()
        self._update_times()

    def _insert_times(self, row_num):
        row = list()
        for col in range(self.times_interval_table.columnCount()-2):
            try:
                row.append(self.times_interval_table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count*int(len(records) == 0)
        if count > 0:
            try:
                self.dataBase.timetable.times.insert(int(row[0]), row[1], row[2])
            except:
                QMessageBox.about(self, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Add: Exists such id")
        self.times_interval_table.resizeRowsToContents()
        self._update_times()

    def _delete_times(self, row_num, id_code):
        count = 0
        records = self.dataBase.timetable.read_by_time(int(id_code))
        count = count+len(records)
        if count == 0:
            try:
                self.dataBase.timetable.times.delete(int(id_code))
            except:
                QMessageBox.about(self, "Error", "Delete: error")
        else:
            QMessageBox.about(self, "Error", "Delete: can't delete: there are foreign keys in timetable")
        self.times_interval_table.resizeRowsToContents()
        self._update_times()



    def _create_teachers_tab(self):
        self.teachers_svbox = QVBoxLayout(self.teachers_tab)
        self.teachers_shbox_table = QHBoxLayout()
        self.teachers_shbox_update = QHBoxLayout()
        self.teachers_svbox.addLayout(self.teachers_shbox_table)
        self.teachers_svbox.addLayout(self.teachers_shbox_update)
        self.teachers_gbox = QGroupBox("Teachers")
        self.teachers_shbox_table.addWidget(self.teachers_gbox)
    
        self._create_teachers_table()
        self.update_teachers_button = QPushButton("Update")
        self.teachers_shbox_update.addWidget(self.update_teachers_button)
        self.update_teachers_button.clicked.connect(self._update_teachers)



    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(len(self.HEADER_NAMES_TEACHERS))
        self.teachers_table.setHorizontalHeaderLabels(self.HEADER_NAMES_TEACHERS)
        self.teachers_mvbox = QVBoxLayout()

        self._update_teachers()

        self.teachers_mvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.teachers_mvbox)

    def _update_teachers(self):
        records = self.dataBase.timetable.teachers.read()

        self.teachers_table.setRowCount(len(records) +1)
        i=0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.teachers_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.teachers_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.teachers_table.setItem(i, 3,QTableWidgetItem(str(r[3])))
            self.teachers_table.setCellWidget(i, 4, update_button)
            update_button.clicked.connect(self._return_lambda_teachers_update(i,r[0]))
            self.teachers_table.setCellWidget(i, 5, delete_button)
            delete_button.clicked.connect(self._return_lambda_teachers_delete(i,r[0]))
            i=i+1
        i=0
        insert_button = QPushButton("Add")
        self.teachers_table.setItem(len(records), 0,QTableWidgetItem(""))
        self.teachers_table.setItem(len(records), 1,QTableWidgetItem(""))
        self.teachers_table.setItem(len(records), 2,QTableWidgetItem(""))
        self.teachers_table.setItem(len(records), 3,QTableWidgetItem(""))
        self.teachers_table.setItem(len(records), 5,QTableWidgetItem(None))
        self.teachers_table.setCellWidget(len(records),4,insert_button)
        insert_button.clicked.connect(self._return_lambda_teachers_insert(len(records)))
        self.teachers_table.resizeRowsToContents()
    
    def _return_lambda_teachers_update(self,i,id_code):
        return lambda: self._change_teachers(i,id_code)
    def _return_lambda_teachers_delete(self,i,id_code):
        return lambda: self._delete_teachers(i,id_code)
    def _return_lambda_teachers_insert(self,r):
        return lambda: self._insert_teachers(r)

    def _change_teachers(self, row_num,id_code):
        row = list()
        for col in range(self.teachers_table.columnCount()-2):
            try:
                row.append(self.teachers_table.item(row_num, col).text())
            except:
                row.append(None)    
        count = 1
        records = self.dataBase.timetable.times.read_by_id(int(row[0]))
        count = count*int(not(len(records)==1 and int(row[0])!=id_code))
        id_dep_value = 0
        if str(row[3]) == 'None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[3])
            records = self.dataBase.timetable.departments.read_by_id(id_dep_value)
            count = count*int(len(records) == 1)
        records = self.dataBase.timetable.subject.read_by_teacher(int(id_code))
        count = count*int(len(records) == 0 or int(row[0]) == id_code)
        if count > 0:
            try:
                self.dataBase.timetable.teachers.update(int(row[0]), row[1], row[2], id_dep_value, int(id_code))
            except:
                QMessageBox.about(self, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Update: Exists such id")
        self.teachers_table.resizeRowsToContents()
        self._update_teachers()

    def _insert_teachers(self, row_num):
        row = list()
        for col in range(self.teachers_table.columnCount()-2):
            try:
                row.append(self.teachers_table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.teachers.read_by_id(int(row[0]))
        count = count*int(len(records) == 0)
        id_dep_value=0
        if str(row[3])=='None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[3])
            records = self.dataBase.timetable.departments.read_by_id(id_dep_value)
            count=count*int(len(records) == 1)
        if count>0:
            try:
                self.dataBase.timetable.teachers.insert((row[0]), row[1], row[2], id_dep_value)
            except:
                QMessageBox.about(self, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Add: Exists such id")
        self.teachers_table.resizeRowsToContents()
        self._update_teachers()

    def _delete_teachers(self,row_num,id_code):
        count = 0
        records = self.dataBase.timetable.subject.read_by_teacher(int(id_code))
        count = count+len(records)
        if count == 0:
            try:
                self.dataBase.timetable.teachers.delete(int(id_code))
            except:
                QMessageBox.about(self, "Error", "Delete: error")
        else:
            QMessageBox.about(self, "Error", "Delete: can't delete: there are foreign keys in subjects")
        self.teachers_table.resizeRowsToContents()
        self._update_teachers()



    def _create_dep_tab(self):
        self.dep_svbox = QVBoxLayout(self.dep_tab)
        self.dep_shbox_table = QHBoxLayout()
        self.dep_shbox_update = QHBoxLayout()
        self.dep_svbox.addLayout(self.dep_shbox_table)
        self.dep_svbox.addLayout(self.dep_shbox_update)
        self.dep_gbox = QGroupBox("Departments")
        self.dep_shbox_table.addWidget(self.dep_gbox)
        self._create_dep_table()
        self.update_dep_button = QPushButton("Update")
        self.dep_shbox_update.addWidget(self.update_dep_button)
        self.update_dep_button.clicked.connect(self._update_dep)


    def _create_dep_table(self):
        self.dep_table = QTableWidget()
        self.dep_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.dep_table.setColumnCount(len(self.HEADER_NAMES_DEPS))
        self.dep_table.setHorizontalHeaderLabels(self.HEADER_NAMES_DEPS)
        self.dep_mvbox = QVBoxLayout()
        self._update_dep()
        self.dep_mvbox.addWidget(self.dep_table)
        self.dep_gbox.setLayout(self.dep_mvbox)

    def _update_dep(self):
        records = self.dataBase.timetable.departments.read()

        self.dep_table.setRowCount(len(records) + 1)
        i=0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.dep_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.dep_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.dep_table.setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.dep_table.setCellWidget(i, 3, update_button)
            update_button.clicked.connect(self._return_lambda_dep_update(i,r[0]))
            self.dep_table.setCellWidget(i, 4, delete_button)
            delete_button.clicked.connect(self._return_lambda_dep_delete(i,r[0]))
            i=i+1
        i=0
        insert_button = QPushButton("Add")
        self.dep_table.setItem(len(records), 0,QTableWidgetItem(""))
        self.dep_table.setItem(len(records), 1,QTableWidgetItem(""))
        self.dep_table.setItem(len(records), 2,QTableWidgetItem(""))
        self.dep_table.setItem(len(records), 4,QTableWidgetItem(None))
        self.dep_table.setCellWidget(len(records),3,insert_button)
        insert_button.clicked.connect(self._return_lambda_dep_insert(len(records)))
        self.dep_table.resizeRowsToContents()
    
    def _return_lambda_dep_update(self,i,id_code):
        return lambda: self._change_dep(i,id_code)
    def _return_lambda_dep_delete(self,i,id_code):
        return lambda: self._delete_dep(i,id_code)
    def _return_lambda_dep_insert(self,r):
        return lambda: self._insert_dep(r)

    def _change_dep(self, row_num,id_code):
        row = list()
        for col in range(self.dep_table.columnCount()-2):
            try:
                row.append(self.dep_table.item(row_num, col).text())
            except:
                row.append(None)
        #print(id_code) 
        #print(row_num)        
        count = 1
        records = self.dataBase.timetable.teachers.read_by_id(int(row[0]))
        count = count*int(not(len(records) == 1 and int(row[0]) != id_code))
        records = self.dataBase.timetable.teachers.read_by_depart(int(id_code))
        count = count*int(len(records) == 0 or int(row[0]) == id_code)
        if count > 0:
            try:
                self.dataBase.timetable.departments.update(int(row[0]), row[1], row[2], int(id_code))
            except:
                QMessageBox.about(self, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Update: Exists such id")
        self.dep_table.resizeRowsToContents()
        self._update_dep()

    def _insert_dep(self, row_num):
        row = list()
        for col in range(self.dep_table.columnCount()-2):
            try:
                row.append(self.dep_table.item(row_num, col).text())
            except:
                row.append(None)
        count = 1
        records = self.dataBase.timetable.departments.read_by_id(int(row[0]))
        count = count*int(len(records) == 0)
        if count > 0:
            try:
                self.dataBase.timetable.departments.insert(int(row[0]), row[1], row[2])
            except:
                QMessageBox.about(self, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Add: Exists such id")
        self.dep_table.resizeRowsToContents()
        self._update_dep()

    def _delete_dep(self,row_num,id_code):
        count = 0
        records = self.dataBase.timetable.teachers.read_by_depart(int(id_code))
        count = count+len(records)
        if count == 0:
            try:
                self.dataBase.timetable.departments.delete(int(id_code))
            except:
                QMessageBox.about(self, "Error", "Delete: error")
        else:
            QMessageBox.about(self, "Error", "Delete: can't delete: there are foreign keys in timetable")
        self.dep_table.resizeRowsToContents()
        self._update_dep()


####
    def _create_subj_tab(self):
        self.subj_svbox = QVBoxLayout(self.subj_tab)
        self.subj_shbox_table = QHBoxLayout()
        self.subj_shbox_update = QHBoxLayout()
        self.subj_svbox.addLayout(self.subj_shbox_table)
        self.subj_svbox.addLayout(self.subj_shbox_update)
        self.subj_gbox = QGroupBox("Subjects")
        self.subj_shbox_table.addWidget(self.subj_gbox)
    
        self._create_subj_table()
        self.update_subj_button = QPushButton("Update")
        self.subj_shbox_update.addWidget(self.update_subj_button)
        self.update_subj_button.clicked.connect(self._update_subj)



    def _create_subj_table(self):
        self.subj_table = QTableWidget()
        self.subj_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subj_table.setColumnCount(len(self.HEADER_NAMES_SUBJ))
        self.subj_table.setHorizontalHeaderLabels(self.HEADER_NAMES_SUBJ)
        self.subj_mvbox = QVBoxLayout()

        self._update_subj()

        self.subj_mvbox.addWidget(self.subj_table)
        self.subj_gbox.setLayout(self.subj_mvbox)

    def _update_subj(self):
        records = self.dataBase.timetable.subject.read()

        self.subj_table.setRowCount(len(records) +1)
        i=0
        for r in records:
            r = list(r)
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            self.subj_table.setItem(i, 0,QTableWidgetItem(str(r[0])))
            self.subj_table.setItem(i, 1,QTableWidgetItem(str(r[1])))
            self.subj_table.setItem(i, 2,QTableWidgetItem(str(r[2])))
            self.subj_table.setCellWidget(i, 3, update_button)
            update_button.clicked.connect(self._return_lambda_subj_update(i,r[0]))
            self.subj_table.setCellWidget(i, 4, delete_button)
            delete_button.clicked.connect(self._return_lambda_subj_delete(i,r[0]))
            i=i+1
        i=0
        insert_button = QPushButton("Add")
        self.subj_table.setItem(len(records), 0,QTableWidgetItem(""))
        self.subj_table.setItem(len(records), 1,QTableWidgetItem(""))
        self.subj_table.setItem(len(records), 2,QTableWidgetItem(""))
        self.subj_table.setItem(len(records), 4,QTableWidgetItem(None))
        self.subj_table.setCellWidget(len(records),3,insert_button)
        insert_button.clicked.connect(self._return_lambda_subj_insert(len(records)))
        self.subj_table.resizeRowsToContents()
    
    def _return_lambda_subj_update(self,i,id_code):
        return lambda: self._change_subj(i,id_code)
    def _return_lambda_subj_delete(self,i,id_code):
        return lambda: self._delete_subj(i,id_code)
    def _return_lambda_subj_insert(self,r):
        return lambda: self._insert_subj(r)

    def _change_subj(self, row_num,id_code):
        row = list()
        for col in range(self.subj_table.columnCount()-2):
            try:
                row.append(self.subj_table.item(row_num, col).text())
            except:
                row.append(None)  
        count=1
        records = self.dataBase.timetable.subject.read_by_id(int(row[0]))
        count=count*int(not(len(records)==1 and int(row[0])!=id_code))
        id_dep_value=0
        if str(row[2])=='None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[2])
            records = self.dataBase.timetable.teachers.read_by_id(id_dep_value)
            count=count*int(len(records)==1)
        records = self.dataBase.timetable.read_by_subject(int(id_code))
        count=count*int(len(records)==0 or int(row[0])==id_code)
        if count>0:

            try:
                self.dataBase.timetable.subject.update(int(row[0]), row[1], id_dep_value, int(id_code))
            except:
                QMessageBox.about(self, "Error", "Update: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Update: Exists such id")
        self.subj_table.resizeRowsToContents()
        self._update_subj()

    def _insert_subj(self, row_num):
        row = list()
        for col in range(self.subj_table.columnCount()-2):
            try:
                row.append(self.subj_table.item(row_num, col).text())
            except:
                row.append(None)
        count=1
        records = self.dataBase.timetable.subject.read_by_id(int(row[0]))
        count=count*int(len(records)==0)
        id_dep_value=0
        if str(row[2])=='None':
            id_dep_value = 'NULL'
        else:
            id_dep_value = int(row[2])
            records = self.dataBase.timetable.teachers.read_by_id(id_dep_value)
            count=count*int(len(records)==1)
        if count>0:
            try:
                self.dataBase.timetable.subject.insert(int(row[0]), row[1], id_dep_value)
            except:
                QMessageBox.about(self, "Error", "Add: Enter all fields")
        else:
            QMessageBox.about(self, "Error", "Add: Exists such id")
        self.subj_table.resizeRowsToContents()
        self._update_subj()

    def _delete_subj(self,row_num,id_code):
        count=0
        records = self.dataBase.timetable.read_by_subject(int(id_code))
        count=count+len(records)
        if count == 0:
            try:
                self.dataBase.timetable.subject.delete(int(id_code))
            except:
                QMessageBox.about(self, "Error", "Delete: error")
        else:
            QMessageBox.about(self, "Error", "Delete: can't delete: there are foreign keys in subjects")
        self.subj_table.resizeRowsToContents()
        self._update_subj()








    def _update_tt(self):
        for week in range(0,WEEKS_NUMBER):
            for day in range(0,DAYS_NUMBER):
                self._update_tt_day_table(week,day)
        #self._update_times()
        #self._update_teachers()
        #self._update_subj()
        #self._update_dep()





   
    def _create_all_objects(self):
        self.tabs = QTabWidget(self)
        self.tt_week_tabs =[ QWidget(self) for week in range(0,WEEKS_NUMBER)]
        self.times_tab = QWidget(self)
        self.subj_tab = QWidget(self)
        self.teachers_tab = QWidget(self)
        self.dep_tab = QWidget(self)
        
        for week in range(0,WEEKS_NUMBER):
            self.tabs.addTab(self.tt_week_tabs[week], f"Timetable week {week}")
        self.tabs.addTab(self.times_tab, "Times")
        self.tabs.addTab(self.subj_tab, "Subjects")
        self.tabs.addTab(self.teachers_tab, "Teachers")
        self.tabs.addTab(self.dep_tab, "Departments")

        self.vbox.addWidget(self.tabs)

        self.tt_weeks_day_tabs = [ QTabWidget(self.tt_week_tabs[week]) for week in range(0,WEEKS_NUMBER)]

        self.tt_week_svbox = [ QVBoxLayout(self.tt_week_tabs[week]) for week in range(0,WEEKS_NUMBER)]
        self.tt_week_shbox_tabs = [ QHBoxLayout() for week in range(0,WEEKS_NUMBER)]
        self.tt_week_shbox_update = [ QHBoxLayout(self.tt_week_tabs[week]) for week in range(0,WEEKS_NUMBER)]
        self.tt_update_buttons = [ QPushButton("Update") for week in range(0,WEEKS_NUMBER)]

        self.tt_day_tabs = [[QWidget() for day in range(0,DAYS_NUMBER)] for week in range(0,WEEKS_NUMBER)]

        self.tt_day_gboxes = [[QGroupBox(DAYS_NAMES[day],self.tt_day_tabs[week][day]) for day in range(0,DAYS_NUMBER)] for week in range(0,WEEKS_NUMBER)]
        self.tt_day_mvbox = [[QVBoxLayout(self.tt_day_gboxes[week][day]) for day in range(0,DAYS_NUMBER)] for week in range(0,WEEKS_NUMBER)]
        self.tt_day_table = [[QTableWidget() for day in range(0,DAYS_NUMBER)] for week in range(0,WEEKS_NUMBER)]

        self.HEADER_NAMES_TT = ["N", "Subject_id", "Room","id","",""]
        self.HEADER_NAMES_TEACHERS = ["id","Surname", "Name", "Dep_id","",""]
        self.HEADER_NAMES_TIMES = ["id","start", "end","",""]
        self.HEADER_NAMES_DEPS = ["id","link", "room","",""]
        self.HEADER_NAMES_SUBJ = ["id","name", "Teacher_id","",""]

        

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
