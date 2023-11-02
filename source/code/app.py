import sys, json, os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5 import QtCore
from PyQt5 import QtGui

from DataBaseConnect.Database import Database
from View.Subjects import Subjects
from View.Teachers import Teachers
from View.Departments import Departments
from View.Times import Times
from View.Timetable import Timetable

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QLabel)

DAYS_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
WEEKS_NUMBER = 2  # WARNING! db has only two weeks as bool field
# for over tt_db - you must change _week_to_type_bool too
DAYS_NUMBER = len(DAYS_NAMES)


class MainWindow(QWidget):
    global DAYS_NAMES, WEEKS_NUMBER, DAYS_NUMBER

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('../img/timetable-icon.png'))
        self.setStyleSheet("background-color: #ede9f2;")
        self.setWindowTitle("Расписание")
        # self.update_times_button.setStyleSheet("""
        #             QPushButton {
        #                 background-color: #e2dce6;
        #             }
        #             QPushButton:hover {
        #                 color: #a164ed;
        #             }
        #             """)
        # self.update_teachers_button.setStyleSheet("""
        #                     QPushButton {
        #                         background-color: #e2dce6;
        #                     }
        #                     QPushButton:hover {
        #                         color: #a164ed;
        #                     }
        #                     """)
        # self.update_teachers_button.setStyleSheet("""
        #                             QPushButton {
        #                                 background-color: #e2dce6;
        #                             }
        #                             QPushButton:hover {
        #                                 color: #a164ed;
        #                             }
        #                             """)
        # self.update_dep_button.setStyleSheet("""
        #                             QPushButton {
        #                                 background-color: #e2dce6;
        #                             }
        #                             QPushButton:hover {
        #                                 color: #a164ed;
        #                             }
        #                             """)
        # self.update_subj_button.setStyleSheet("""
        #                             QPushButton {
        #                                 background-color: #e2dce6;
        #                             }
        #                             QPushButton:hover {
        #                                 color: #a164ed;
        #                             }
        #                             """)
        # self.tt_update_buttons.setStyleSheet("""
        #                             QPushButton {
        #                                 background-color: #e2dce6;
        #                             }
        #                             QPushButton:hover {
        #                                 color: #a164ed;
        #                             }
        #                             """)


        entry_data = str(os.path.dirname(os.path.abspath(__file__)))
        entry_data += "/DataBaseConnect/options_for_connect.json"
        entry_data = os.path.normpath(entry_data)

        entry_data = open(entry_data, "r")
        entry_data = json.load(entry_data)
        # self.dataBase = Database(entry_data)

        self.vbox = QVBoxLayout(self)

        self._create_all_objects()

        for week in range(0, WEEKS_NUMBER):
            self._create_tt_week_tab(week)
        self._create_times_tab()
        self._create_subj_tab()
        self._create_teachers_tab()
        self._create_dep_tab()

    def _week_to_type_bool(self, week):  # change if db has another week field then boolean
        if week == 1:
            return "TRUE"
        elif week == 0:
            return "FALSE"
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setInformativeText("No such week in this db")
            self.msg.setText("Error")
            self.msg.setWindowTitle("Error")

    def _create_tt_week_tab(self, week):
        for day in range(0, DAYS_NUMBER):
            self.tt_weeks_day_tabs[week].addTab(self.tt_day_tabs[week][day], DAYS_NAMES[day])

        self.tt_week_svbox[week].addLayout(self.tt_week_shbox_tabs[week])
        self.tt_week_svbox[week].addLayout(self.tt_week_shbox_update[week])
        self.tt_week_shbox_tabs[week].addWidget(self.tt_weeks_day_tabs[week])
        self.tt_week_shbox_update[week].addWidget(self.tt_update_buttons[week])
        self.tt_update_buttons[week].clicked.connect(self._update_tt)

        for day in range(0, DAYS_NUMBER):
            self._create_day_tab(week, day)

    def _create_day_tab(self, week, day):
        self.tt_day_table[week][day].setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tt_day_table[week][day].setColumnCount(len(self.HEADER_NAMES_TT))
        self.tt_day_table[week][day].setHorizontalHeaderLabels(self.HEADER_NAMES_TT)

        self.timetables[week][day].update_tt_day_table()

        self.tt_day_mvbox[week][day].addWidget(self.tt_day_table[week][day])
        self.tt_day_gboxes[week][day].setLayout(self.tt_day_mvbox[week][day])

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
        self.update_times_button.clicked.connect(self.times.update_times)

    def _create_times_table(self):
        self.times_interval_table = QTableWidget()
        self.times_interval_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.times_interval_table.setColumnCount(len(self.HEADER_NAMES_TIMES))
        self.times_interval_table.setHorizontalHeaderLabels(self.HEADER_NAMES_TIMES)
        self.times_mvbox = QVBoxLayout()
        self.times_mvbox.addWidget(self.times_interval_table)
        self.times_gbox.setLayout(self.times_mvbox)

        self.times = Times(self.dataBase, self.times_interval_table)

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
        self.update_teachers_button.clicked.connect(self.teachers.update_teachers)

    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(len(self.HEADER_NAMES_TEACHERS))
        self.teachers_table.setHorizontalHeaderLabels(self.HEADER_NAMES_TEACHERS)
        self.teachers_mvbox = QVBoxLayout()

        self.teachers_mvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.teachers_mvbox)

        self.teachers = Teachers(self.dataBase, self.teachers_table)

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
        self.update_dep_button.clicked.connect(self.departments.update_dep)

    def _create_dep_table(self):
        self.dep_table = QTableWidget()
        self.dep_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.dep_table.setColumnCount(len(self.HEADER_NAMES_DEPS))
        self.dep_table.setHorizontalHeaderLabels(self.HEADER_NAMES_DEPS)
        self.dep_mvbox = QVBoxLayout()
        self.dep_mvbox.addWidget(self.dep_table)
        self.dep_gbox.setLayout(self.dep_mvbox)

        self.departments = Departments(self.dataBase, self.dep_table)

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
        self.update_subj_button.clicked.connect(self.subjects.update_subj)

    def _create_subj_table(self):
        self.subj_table = QTableWidget()
        self.subj_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subj_table.setColumnCount(len(self.HEADER_NAMES_SUBJ))
        self.subj_table.setHorizontalHeaderLabels(self.HEADER_NAMES_SUBJ)
        self.subj_mvbox = QVBoxLayout()

        self.subj_mvbox.addWidget(self.subj_table)
        self.subj_gbox.setLayout(self.subj_mvbox)

        self.subjects = Subjects(self.dataBase, self.subj_table)

    def _update_tt(self):
        for week in range(0, WEEKS_NUMBER):
            for day in range(0, DAYS_NUMBER):
                self.timetables[week][day].update_tt_day_table()

    def _create_all_objects(self):
        self.tabs = QTabWidget(self)
        self.tt_week_tabs = [QWidget(self) for week in range(0, WEEKS_NUMBER)]
        self.times_tab = QWidget(self)
        self.subj_tab = QWidget(self)
        self.teachers_tab = QWidget(self)
        self.dep_tab = QWidget(self)

        for week in range(0, WEEKS_NUMBER):
            self.tabs.addTab(self.tt_week_tabs[week], f"Timetable week {week}")
        self.tabs.addTab(self.times_tab, "Times")
        self.tabs.addTab(self.subj_tab, "Subjects")
        self.tabs.addTab(self.teachers_tab, "Teachers")
        self.tabs.addTab(self.dep_tab, "Departments")

        self.vbox.addWidget(self.tabs)

        self.tt_weeks_day_tabs = [QTabWidget(self.tt_week_tabs[week]) for week in range(0, WEEKS_NUMBER)]

        self.tt_week_svbox = [QVBoxLayout(self.tt_week_tabs[week]) for week in range(0, WEEKS_NUMBER)]
        self.tt_week_shbox_tabs = [QHBoxLayout() for week in range(0, WEEKS_NUMBER)]
        self.tt_week_shbox_update = [QHBoxLayout(self.tt_week_tabs[week]) for week in range(0, WEEKS_NUMBER)]
        self.tt_update_buttons = [QPushButton("Update") for week in range(0, WEEKS_NUMBER)]

        self.tt_day_tabs = [[QWidget() for day in range(0, DAYS_NUMBER)] for week in range(0, WEEKS_NUMBER)]

        self.tt_day_gboxes = [[QGroupBox(DAYS_NAMES[day], self.tt_day_tabs[week][day]) for day in range(0, DAYS_NUMBER)]
                              for week in range(0, WEEKS_NUMBER)]
        self.tt_day_mvbox = [[QVBoxLayout(self.tt_day_gboxes[week][day]) for day in range(0, DAYS_NUMBER)] for week in
                             range(0, WEEKS_NUMBER)]
        self.tt_day_table = [[QTableWidget() for day in range(0, DAYS_NUMBER)] for week in range(0, WEEKS_NUMBER)]
        self.timetables = [
            [Timetable(self.dataBase, self.tt_day_table[week][day], week, day) for day in range(0, DAYS_NUMBER)] for
            week in range(0, WEEKS_NUMBER)]

        self.HEADER_NAMES_TT = ["N", "Subject_id", "Room", "id", "", ""]
        self.HEADER_NAMES_TEACHERS = ["id", "Surname", "Name", "Dep_id", "", ""]
        self.HEADER_NAMES_TIMES = ["id", "start", "end", "", ""]
        self.HEADER_NAMES_DEPS = ["id", "link", "room", "", ""]
        self.HEADER_NAMES_SUBJ = ["id", "name", "Teacher_id", "", ""]

        self.update_times_button.setStyleSheet("""
                            QPushButton {
                                background-color: #e2dce6;
                            }
                            QPushButton:hover {
                                color: #a164ed;
                            }
                            """)
        self.update_teachers_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #e2dce6;
                                    }
                                    QPushButton:hover {
                                        color: #a164ed;
                                    }
                                    """)
        self.update_teachers_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #e2dce6;
                                            }
                                            QPushButton:hover {
                                                color: #a164ed;
                                            }
                                            """)
        self.update_dep_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #e2dce6;
                                            }
                                            QPushButton:hover {
                                                color: #a164ed;
                                            }
                                            """)
        self.update_subj_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #e2dce6;
                                            }
                                            QPushButton:hover {
                                                color: #a164ed;
                                            }
                                            """)
        self.tt_update_buttons.setStyleSheet("""
                                            QPushButton {
                                                background-color: #e2dce6;
                                            }
                                            QPushButton:hover {
                                                color: #a164ed;
                                            }
                                            """)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
