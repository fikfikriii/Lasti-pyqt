import math
import sqlite3
import sys

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

bg_color = '#28293D'
atlantic = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
light_yellow = '#FFD9A0'
light_gum = '#FF8BD5'
btn_color = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
btn_color_hover = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'


class WorkoutHistory(QWidget):
    switch = pyqtSignal(str, dict)

    def __init__(self, user=None):
        super().__init__()
        if (user != None):
            self.user = user
        else:
            self.user = {
                "id": "-1",
                "fullname": "John Doe",
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "johndoe",
                "type": "user"
            }
        self.conn = sqlite3.connect("fitpal.db")
        self.fetchWorkoutHistory()
        self.currPage = 0
        self.setUpDashboardWindow()

    def fetchWorkoutHistory(self):
        # Mengambil workout history yang dimiliki oleh user
        self.history = []
        c = self.conn.cursor()
        c.execute(f"""
    SELECT *
    FROM workout_history
    WHERE user_id = {self.user["id"]}
    """)
        res = c.fetchall()
        for r in res:
            d = {
                "history_id": r[0],
                "user_id": r[1],
                "olahraga_id": r[2],
                "name": r[3],
                "specification": r[4],
                "date": r[5]
            }
            self.history.append(d)

    def updateWorkoutHistory(self):
        self.fetchWorkoutHistory()
        self.updateCards()

    def setUpDashboardWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("FitPal - Workout History")
        self.setUpWidgets()

    def setUpWidgets(self):
        # Fonts
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
        # Set up background image
        self.setStyleSheet(f"background-color: {bg_color}")
        # Set up logo
        logoPixmap = QPixmap("../img/dashboard-fitpal-logo.png")
        logo = QLabel(self)
        logo.setPixmap(logoPixmap)
        logo.move(60, 30)
        logo.setStyleSheet(f"background-color: {bg_color}")
        # Set up hello label
        self.helloLabel = QLabel(self)
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")
        self.helloLabel.move(635, 44)
        self.helloLabel.setStyleSheet(
            f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}')
        self.helloLabel.setFixedSize(585, 29)
        self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.helloLabel.setFont(inter24)
        # Set up heading label
        heading = QLabel(self)
        heading.setText("Workout History")
        heading.move(60, 120)
        heading.setStyleSheet(
            f"color: {atlantic}; background-color: {bg_color}")
        heading.setFont(inter48)
        # Set up log out button
        logOutBtn = QPushButton(self)
        logOutBtn.setText("Log Out")
        logOutBtn.setStyleSheet(f'''
      QPushButton {{
        color: #ffffff;
        background-color: {btn_color};
        border: none;
        border-radius: 12px;
      }}
      QPushButton:hover {{
        background-color: {btn_color_hover};
      }}
    ''')
        logOutBtn.setFixedSize(121, 48)
        logOutBtn.setFont(inter16)
        logOutBtn.move(1099, 88)
        logOutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logOutBtn.clicked.connect(self.logOut)
        # Set up no history found label
        self.noHistoryFound = QLabel(self)
        self.noHistoryFound.setText(
            "You haven't completed any workout yet!\nPlease add a new workout to your history.")
        self.noHistoryFound.move(105, 208)
        self.noHistoryFound.setStyleSheet(
            f'color: rgba(255, 255, 255, 0.8); background-color:{bg_color}')
        self.noHistoryFound.setFont(inter24)
        self.noHistoryFound.hide()
        # Set up back button
        self.backBtn = QPushButton(self)
        self.backBtn.setText("Back")
        self.backBtn.setStyleSheet('''
    QPushButton {
      color: #ffffff;
      background-color: #F10628;
      border: none;
      border-radius: 12px;
    }
    QPushButton:hover {
      background-color: #f43853;
    }
    ''')
        self.backBtn.setFont(inter16)
        self.backBtn.setFixedSize(103, 48)
        self.backBtn.move(60, 612)
        self.backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.backBtn.clicked.connect(self.backToDashboard)
        # Set up back button
        self.addHistoryBtn = QPushButton(self)
        self.addHistoryBtn.setText("Add workout history")
        self.addHistoryBtn.setStyleSheet('''
    QPushButton {
      color: #ffffff;
      background-color: qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);
      border: none;
      border-radius: 12px;
    }
    QPushButton:hover {
      background-color: qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff);
    }
    ''')
        self.addHistoryBtn.setFont(inter16)
        self.addHistoryBtn.setFixedSize(212, 48)
        self.addHistoryBtn.move(178, 612)
        self.addHistoryBtn.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.addHistoryBtn.clicked.connect(self.toAddWorkout)

        self.setUpCards()

    def backToDashboard(self):
        self.switch.emit("user_dashboard", self.user)

    def toAddWorkout(self):
        self.switch.emit("add_history", self.user)

    def setUpCards(self):
        # Set up cards
        self.cards = [{}, {}, {}]
        for i in range(3):
            inter18 = QFont()
            inter18.setFamily("Inter")
            inter18.setPixelSize(18)

            inter20b = QFont()
            inter20b.setFamily("Inter")
            inter20b.setPixelSize(20)
            inter20b.setBold(True)

            inter16 = QFont()
            inter16.setFamily("Inter")
            inter16.setPixelSize(16)

            pixmap = QPixmap("../img/grape_card.png")
            translateX = i * 304
            self.cards[i]['cardLabel'] = QLabel(self)
            self.cards[i]['cardLabel'].setPixmap(pixmap)
            self.cards[i]['cardLabel'].move(191 + translateX, 235)

            img = QPixmap("../img/push-up.png")
            self.cards[i]['cardImg'] = QLabel(self)
            self.cards[i]['cardImg'].setPixmap(img)
            self.cards[i]['cardImg'].move(256 + translateX, 260)
            self.cards[i]['cardImg'].setFixedSize(160, 160)
            self.cards[i]['cardImg'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cards[i]['cardImg'].setStyleSheet("background-color: #7366FE")

            self.cards[i]['date'] = QLabel(self)
            self.cards[i]['date'].setText("20 April 2022")
            self.cards[i]['date'].setFixedWidth(229)
            self.cards[i]['date'].setFont(inter20b)
            self.cards[i]['date'].move(221 + translateX, 455)
            self.cards[i]['date'].setStyleSheet(
                "background-color: #A19AFE; color: rgba(0, 0, 0, 0.5)")

            self.cards[i]['name'] = QLabel(self)
            self.cards[i]['name'].setText("Push up")
            self.cards[i]['name'].setFixedWidth(229)
            self.cards[i]['name'].setFont(inter18)
            self.cards[i]['name'].move(221 + translateX, 478)
            self.cards[i]['name'].setStyleSheet(
                "background-color: #A19AFE; color: rgba(0, 0, 0, 0.5)")

            self.cards[i]['specification'] = QLabel(self)
            self.cards[i]['specification'].setText("12 repetitions")
            self.cards[i]['specification'].setFixedWidth(229)
            self.cards[i]['specification'].setFont(inter16)
            self.cards[i]['specification'].move(221 + translateX, 520)
            self.cards[i]['specification'].setStyleSheet(
                "background-color: #A19AFE; color: rgba(0, 0, 0, 0.5)")

        # Set up left and right button
        self.leftButton = QPushButton(self)
        self.leftButton.setIcon(QIcon("../img/left-btn.png"))
        self.leftButton.move(143, 371)
        self.leftButton.setFixedSize(48, 48)
        self.leftButton.setStyleSheet("background-color: #373951")
        self.leftButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.leftButton.clicked.connect(self.prevPage)

        self.rightButton = QPushButton(self)
        self.rightButton.setIcon(QIcon("../img/right-btn.png"))
        self.rightButton.move(1088, 371)
        self.rightButton.setFixedSize(48, 48)
        self.rightButton.setStyleSheet("background-color: #373951")
        self.rightButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.rightButton.clicked.connect(self.nextPage)

        self.updateCards()

    def updateCards(self):
        pages = math.ceil(len(self.history) / 3)
        # Hide button sesuai page
        if (self.currPage == 0):
            self.leftButton.hide()
            self.rightButton.show()
        elif (self.currPage == pages - 1):
            self.rightButton.hide()
            self.leftButton.show()
        else:
            self.leftButton.show()
            self.rightButton.show()
        # Apabila pages = 1
        if pages == 1 or pages == 0:
            self.leftButton.hide()
            self.rightButton.hide()

        # Lakukan pengubahan pada card
        for i in range(3):
            hIndex = self.currPage * 3 + i
            if hIndex >= len(self.history):
                self.cards[i]['cardLabel'].hide()
                self.cards[i]['cardImg'].hide()
                self.cards[i]['date'].hide()
                self.cards[i]['name'].hide()
                self.cards[i]['specification'].hide()
            else:
                # Lakukan perubahan!
                if self.history[hIndex]['olahraga_id'] == -1:
                    self.cards[i]['cardImg'].setPixmap(
                        QPixmap("../img/weightlifting.png"))
                    self.cards[i]['name'].setText(self.history[hIndex]['name'])
                else:
                    # Fetch olahraga yang bersangkutan
                    c = self.conn.cursor()
                    c.execute(f"""
          SELECT *
          FROM list_olahraga
          WHERE olahraga_id = {self.history[hIndex]['olahraga_id']}
          """)
                    res = c.fetchone()
                    if (res[4][:4] == 'http'):
                        pixmap = QPixmap()
                        request = requests.get(res[4])
                        pixmap.loadFromData(request.content)
                        pixmap.scaledToHeight(120)
                        self.cards[i]["cardImg"].setPixmap(
                            pixmap.scaledToHeight(160))
                    else:
                        self.cards[i]['cardImg'].setPixmap(QPixmap(res[4]))
                    self.cards[i]['name'].setText(res[1])
                self.cards[i]['date'].setText(self.history[hIndex]['date'])
                self.cards[i]['specification'].setText(
                    self.history[hIndex]['specification'])
                # Tunjukkan card
                self.cards[i]['cardLabel'].show()
                self.cards[i]['cardImg'].show()
                self.cards[i]['date'].show()
                self.cards[i]['name'].show()
                self.cards[i]['specification'].show()

        if len(self.history) == 0:
            self.noHistoryFound.show()
        else:
            self.noHistoryFound.hide()

    def prevPage(self):
        self.currPage -= 1
        self.updateCards()

    def nextPage(self):
        self.currPage += 1
        self.updateCards()

    def updateUser(self, user):
        self.user = user
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")

    def logOut(self):
        self.switch.emit("login", {})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkoutHistory()
    window.show()
    sys.exit(app.exec())
