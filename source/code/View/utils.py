from PyQt5.QtWidgets import QMessageBox


def week_to_type_bool(week):  # change if db has another week field then boolean
    if week == 1:
        return "TRUE"
    elif week == 0:
        return "FALSE"
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setInformativeText("no such week in this db")
        msg.setText("Error")
        msg.setWindowTitle("Error")
