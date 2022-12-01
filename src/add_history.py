import sqlite3
import sys
from datetime import date

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QDateEdit, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QWidget)

# defined style
bg_color = '#28293D'
white = '#FFF'
atlantic = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
light_yellow = '#FFD9A0'
light_purple = '#A19AFE'
primary_red = '#F10628'
primary_red_hover = "#f43853"
btn_color = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
btn_color_hover = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'
hello_label_style = f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}'
logout_btn_style = '''
      QPushButton {
        color: #ffffff;
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);
        border: none;
        border-radius: 12px;
      }
      QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff);
      }
    '''
back_btn_style = f'''
      QPushButton {{
        color: #ffffff;
        background-color: {primary_red};
        border: none;
        border-radius: 12px;
      }}
      QPushButton:hover {{
        background-color: {primary_red_hover};
      }}
    '''
card_content_style = "color: #FFF; background-color: #3E405B"


class addHistory(QWidget):
    switch = pyqtSignal(str, dict)

    def __init__(self, user=None):
        super().__init__()
        if (user != None):
            self.user = user
        else:
            self.user = {
                "fullname": "John Doe",
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "johndoe",
                "type": "user"
            }
        self.conn = sqlite3.connect("fitpal.db")
        self.setUpDashboardWindow()

    def setUpDashboardWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("FitPal - Finish your workout")
        self.setUpWidgets()

    def setUpWidgets(self):

        # background
        self.setStyleSheet(f'background-color: {bg_color}')

        # font
        inter13 = QFont()
        inter13.setFamily("Inter")
        inter13.setPixelSize(13)

        inter16 = QFont()
        inter16.setFamily("Inter")
        inter16.setPixelSize(16)

        inter24 = QFont()
        inter24.setFamily("Inter")
        inter24.setPixelSize(24)

        inter24bold = QFont()
        inter24bold.setFamily("Inter")
        inter24bold.setPixelSize(24)
        inter24bold.setBold(True)

        inter48 = QFont()
        inter48.setFamily("Inter")
        inter48.setPixelSize(48)
        inter48.setBold(True)
        # end of font

        # logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("../img/dashboard-fitpal-logo.png"))
        self.logo.move(60, 30)
        self.logo.setStyleSheet(f"background-color: {bg_color}")
        # end of logo

        # title
        self.title = QLabel(self)
        self.title.setText("Finish your workout")
        self.title.setFont(inter48)
        self.title.setStyleSheet(
            f"color: {atlantic}; background-color: {bg_color}")
        self.title.move(60, 120)
        # end of title

        # subtitle
        self.subtitle = QLabel(self)
        self.subtitle.setText(
            "Please fill out this required form for adding the workout to your history")
        self.subtitle.setFont(inter24)
        self.subtitle.move(60, 180)
        self.subtitle.setStyleSheet(
            f"color: #FFFFFF; background-color: {bg_color}")
        # end of subtitle

        # title input
        self.title_input = QLabel(self)
        self.title_input.setText("Title")
        self.title_input.move(400, 250)
        self.title_input.setStyleSheet(
            f"color: {white}; background-color: {bg_color}")
        self.title_input.setFont(inter16)
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Example: Push up / Sit Up")
        self.title_input.setFixedSize(465, 45)
        self.title_input.move(400, 280)
        self.title_input.setStyleSheet('''
          padding: 11px 30px 11px 30px;
          border: 1px solid rgba(255, 255, 255, 0.8);
          color: rgba(255, 255, 255, 0.8);
          background-color: #3E405B
        ''')
        self.title_input.setFont(inter16)
        # end of title input

        # spec input
        self.specification = QLabel(self)
        self.specification.setText("Specification")
        self.specification.move(400, 355)
        self.specification.setStyleSheet(
            f"color: {white}; background-color: {bg_color}")
        self.specification.setFont(inter16)
        self.specification = QLineEdit(self)
        self.specification.setPlaceholderText(
            "Example: 10 km / 5 minutes / 20 repetition")
        self.specification.setFixedSize(465, 45)
        self.specification.move(400, 385)
        self.specification.setStyleSheet('''
          padding: 11px 30px 11px 30px;
          border: 1px solid rgba(255, 255, 255, 0.8);
          color: rgba(255, 255, 255, 0.8);
          background-color: #3E405B
        ''')
        self.specification.setFont(inter16)
        # end of title input

        # date input
        self.date = QLabel(self)
        self.date.setText("Date")
        self.date.move(400, 450)
        self.date.setStyleSheet(
            f"color: {white}; background-color: {bg_color}")
        self.date.setFont(inter16)
        self.date = QDateEdit(self)
        # self.date.setPlaceholderText("Example: 05 January 2022, 01 March 2021")
        self.date.setFixedSize(465, 45)
        self.date.move(400, 480)
        self.date.setStyleSheet('''
          padding: 11px 30px 11px 30px;
          border: 1px solid rgba(255, 255, 255, 0.8);
          color: rgba(255, 255, 255, 0.8);
          background-color: #3E405B
        ''')
        self.date.setFont(inter16)
        self.date.setDate(date.today())
        self.date.setDisplayFormat("yyyy-MM-dd")
        # end of date input

        # back button
        self.backBtn = QPushButton(self)
        self.backBtn.setText("Back")
        self.backBtn.setStyleSheet(back_btn_style)
        self.backBtn.setFont(inter16)
        self.backBtn.setFixedSize(121, 48)
        self.backBtn.move(60, 627)
        self.backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.backBtn.clicked.connect(self.toWorkoutHistory)
        # end of button

        # add new workout btn
        self.addBtn = QPushButton(self)
        self.addBtn.setText("Add to history")
        self.addBtn.setStyleSheet(logout_btn_style)
        self.addBtn.setFont(inter16)
        self.addBtn.setFixedSize(156, 48)
        self.addBtn.move(190, 627)
        self.addBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addBtn.clicked.connect(self.addHistory)
        # end of add new workout

    def updateUser(self, user):
        self.user = user

    def addHistory(self):
        if self.title_input.text() == "" or self.specification.text() == "" or self.date.text() == "":
            self.msgBox = QMessageBox()
            self.msgBox.setText("Please fill out the form properly!")
            self.msgBox.setIcon(QMessageBox.Icon.Warning)
            self.msgBox.setStyleSheet("background-color: white")
            self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msgBox.exec()
            return
        c = self.conn.cursor()
        c.execute(
            f"SELECT * FROM list_olahraga WHERE name = '{self.title_input.text()}'")
        res = c.fetchall()
        if(res == None or res == []):
            # Olahraganya tidak ada
            c.execute(
                f"INSERT INTO workout_history (user_id, olahraga_id, name, specification, date) VALUES ({self.user['id']}, -1, '{self.title_input.text()}', '{self.specification.text()}', '{self.date.text()}')")
        else:
            c.execute(
                f"INSERT INTO workout_history (user_id, olahraga_id, specification, date) VALUES ({self.user['id']}, {res[0][0]}, '{self.specification.text()}', '{self.date.text()}')")

        # close connection and clear
        self.conn.commit()
        self.title_input.clear()
        self.specification.clear()
        self.date.clear()

        # add history succesful
        self.msgBox = QMessageBox()
        self.msgBox.setText("Successfuly added workout to your history!")
        self.msgBox.setWindowTitle(
            "Successfuly added workout to your history!")
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setStyleSheet("background-color: white")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.exec()

        self.toWorkoutHistory()

    def toWorkoutHistory(self):
        self.switch.emit("workout_history", self.user)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addHistory()
    window.show()
    sys.exit(app.exec())
