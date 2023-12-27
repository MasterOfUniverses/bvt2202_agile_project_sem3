import pytest
from source.code.app import MainWindow
from PyQt5 import QtCore


@pytest.fixture
def app_forTest(qtbot):
    app = MainWindow()
    qtbot.addWidget(app)

    return app


def test_Tab1(app_forTest):
    assert app_forTest.tabs.times_tab.text() == "Times"

def test_Tab2(app_forTest):
    assert app_forTest.tabs.subj_tab.text() == "Subjects"

def test_Button(app_forTest):
    assert app_forTest.update_subj_button.text() == "Subjects"
    
def test_TableHeader(app_forTest):
    assert app_forTest.teachers_table.horizontalHeaderItem(1).text() == "Surname"

def test_TableItem(app_forTest):
    assert app_forTest.teachers_table.itemAt(1,0).text() == "Королева"

def test_field_after_change(app_forTest, qtbot):
    # вернуть айтем по координатам, нажать на кнопку 
    # нам неважно название элемента кнопки - teachers.delete_button. просто коорды
    qtbot.mouseClick(app_forTest.teachers_table.itemAt(5,9), QtCore.Qt.LeftButton)
    assert app_forTest.teachers_table.itemAt(1,9).text() != app_forTest.teachers_table.itemAt(1,9).text()

def test_update(app_forTest, qtbot):
    app_forTest.teachers_table.itemAt(1,9).setText("неТренин")
    qtbot.mouseClick(app_forTest.teachers_table.itemAt(4,9), QtCore.Qt.LeftButton)
    assert app_forTest.teachers_table.itemAt(1,9).text() == "неТренин"