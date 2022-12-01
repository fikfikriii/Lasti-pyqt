import sqlite3
import sys
import webbrowser
from datetime import date

import requests
from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QMessageBox, QPushButton,
                             QWidget)

BG_COLOR = '#28293D'
PRIMARY_BLACK = '#000000'
PRIMARY_WHITE = '#FFFFFF'
PRIMARY_BUTTON = '#5561FF'
YELLOW = '#FEC166'
DARK_YELLOW = '#EEA02B'
GRAPE = '#7366FE'
ATLANTIC = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
LIGHT_YELLOW = '#FFD9A0'
BTN_COLOR = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
BTN_COLOR_HOVER = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'

class DisplayWorkout(QWidget):
    switch = pyqtSignal(str, dict)

    def __init__(self, user = None):
        super().__init__()
        if user is not None:
            self.user = user
        else:
            self.user = {
                "fullname": "John Doe",
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "johndoe",
                "type": "user"
            }
        self.conn = sqlite3.connect('fitpal.db')
        self.pageWorkout = 0
        self.pageWorkoutPlan = 0
        self.workoutPlan = []
        self.listWorkoutPlan = None
        self.fetchWorkout()
        self.setUpDisplayWorkoutWindow()

    def updateDisplayWorkout(self):
        self.fetchWorkout()
        self.setUpDisplayWorkout()

    def setUpDisplayWorkoutWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("FitPal - Display Workout")
        self.setUpWidgets()

    def setUpWidgets(self):
        # Fonts
        inter24 = QFont()
        inter24.setFamily("Inter")
        inter24.setPixelSize(24)

        inter16 = QFont()
        inter16.setFamily("Inter")
        inter16.setPixelSize(16)

        # Set up background image
        self.setStyleSheet(f"background-color: {BG_COLOR}")

        # Set up logo
        logoPixmap = QPixmap("../img/dashboard-fitpal-logo.png")
        logo = QLabel(self)
        logo.setPixmap(logoPixmap)
        logo.move(60, 30)
        logo.setStyleSheet(f"background-color: {BG_COLOR}")

        # Set up hello label
        self.helloLabel = QLabel(self)
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")
        self.helloLabel.move(635, 44)
        self.helloLabel.setStyleSheet("color: rgba(255, 255, 255, 0.8); background-color: {BG_COLOR}")
        self.helloLabel.setFixedSize(585, 29)
        self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.helloLabel.setFont(inter24)

        # Set up no workout plan text
        self.noWorkoutPlan = QLabel(self)
        self.noWorkoutPlan.setText("You don’t have any workout plans tailored for you!")
        self.noWorkoutPlan.move(105, 573)
        self.noWorkoutPlan.setStyleSheet("color: rgba(255, 255, 255, 0.8); background-color: {BG_COLOR}")
        self.noWorkoutPlan.setFont(inter24)
        self.noWorkoutPlan.hide()

        # Set up back button
        backBtn = QPushButton(self)
        backBtn.setText("Back")
        backBtn.setStyleSheet(f'''
        QPushButton {{
            color: #ffffff;
            background-color: {BTN_COLOR};
            border: none;
            border-radius: 12px;
        }}
        QPushButton:hover {{
            background-color: {BTN_COLOR_HOVER};
        }}
        ''')
        backBtn.setFixedSize(121, 48)
        backBtn.setFont(inter16)
        backBtn.move(1099, 88)
        backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        backBtn.clicked.connect(self.back)

        self.rightWorkoutButton = QPushButton(self)
        self.rightWorkoutButton.setGeometry(QRect(1130, 308, 48, 48))
        self.rightWorkoutButton.setStyleSheet("background-image: url(../img/right-btn.png);")
        self.rightWorkoutButton.clicked.connect(self.rightWorkoutButtonClicked)
        self.rightWorkoutButton.hide()
        self.rightWorkoutButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.leftWorkoutButton = QPushButton(self)
        self.leftWorkoutButton.setGeometry(QRect(102, 308, 48, 48))
        self.leftWorkoutButton.setStyleSheet("background-image: url(../img/left-btn.png);")
        self.leftWorkoutButton.clicked.connect(self.leftWorkoutButtonClicked)
        self.leftWorkoutButton.hide()
        self.leftWorkoutButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.rightWorkoutPlanButton = QPushButton(self)
        self.rightWorkoutPlanButton.setGeometry(QRect(1130, 590, 48, 48))
        self.rightWorkoutPlanButton.setStyleSheet("background-image: url(../img/right-btn.png);")
        self.rightWorkoutPlanButton.clicked.connect(self.rightWorkoutPlanButtonClicked)
        self.rightWorkoutPlanButton.hide()

        self.leftWorkoutPlanButton = QPushButton(self)
        self.leftWorkoutPlanButton.setGeometry(QRect(102, 590, 48, 48))
        self.leftWorkoutPlanButton.setStyleSheet("background-image: url(../img/left-btn.png);")
        self.leftWorkoutPlanButton.clicked.connect(self.leftWorkoutPlanButtonClicked)
        self.leftWorkoutPlanButton.hide()

        # Set up workout cards from workout
        self.initializeWorkoutCards()
        self.setUpDisplayWorkout()

    def initializeWorkoutCards(self):
        # Set up font
        inter10 = QFont()
        inter10.setFamily("Inter")
        inter10.setPixelSize(10)

        inter12 = QFont()
        inter12.setFamily("Inter")
        inter12.setPixelSize(12)

        inter16bold = QFont()
        inter16bold.setFamily("Inter")
        inter16bold.setPixelSize(16)
        inter16bold.setBold(True)

        inter24bold = QFont()
        inter24bold.setFamily("Inter")
        inter24bold.setPixelSize(24)
        inter24bold.setBold(True)

        inter48 = QFont()
        inter48.setFamily("Inter")
        inter48.setPixelSize(48)
        inter48.setBold(True)

        # Set up heading Workout label
        self.headingTop = QLabel(self)
        self.headingTop.setText("Workout Activity")
        self.headingTop.move(60, 120)
        self.headingTop.setStyleSheet(f"color: {ATLANTIC}; background-color: {BG_COLOR}")
        self.headingTop.setFont(inter48)

        # Set up heading Workout Plan label
        self.headingBottom = QLabel(self)
        self.headingBottom.setText("Workout Plan")
        self.headingBottom.move(60, 500)
        self.headingBottom.setStyleSheet(f"color: {ATLANTIC}; background-color: {BG_COLOR}")
        self.headingBottom.setFont(inter48)

        # Set up workout cards with empty set
        self.workoutCards = []
        for i in range(3):
            self.workoutCards.append({})
            self.workoutCards[i]["card"] = QLabel(self)
            self.workoutCards[i]["card"].setGeometry(QRect(150 + (i * 340), 188, 300, 300))
            self.workoutCards[i]["card"].setStyleSheet(f"background-color: {BG_COLOR}")
            self.workoutCards[i]["card"].setPixmap(QPixmap("../img/template-YELLOW-card.png"))
            self.workoutCards[i]["cardIllustration"] = QLabel(self)
            self.workoutCards[i]["cardIllustration"].setGeometry(QRect(240 + (i%3*340), 200, 120, 120))
            self.workoutCards[i]["cardIllustration"].setStyleSheet(f"background-color: {YELLOW}")
            self.workoutCards[i]["cardIllustration"].setPixmap(QPixmap("../img/push-up.png"))
            self.workoutCards[i]["cardTitle"] = QLabel(self)
            self.workoutCards[i]["cardTitle"].setGeometry(QRect(172 + (i%3*340), 339, 120, 20))
            self.workoutCards[i]["cardTitle"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.workoutCards[i]["cardTitle"].setText("Title")
            self.workoutCards[i]["cardTitle"].setFont(inter16bold)
            self.workoutCards[i]["cardDescription"] = QLabel(self)
            self.workoutCards[i]["cardDescription"].setText("Description")
            self.workoutCards[i]["cardDescription"].setGeometry(QRect(172 + (i%3*340), 366, 256, 64))
            self.workoutCards[i]["cardDescription"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.workoutCards[i]["cardDescription"].setFont(inter10)
            self.workoutCards[i]["cardSpecification"] = QLabel(self)
            self.workoutCards[i]["cardSpecification"].setText("Specification")
            self.workoutCards[i]["cardSpecification"].setGeometry(QRect(350 + (i*340), 344, 80, 14))
            self.workoutCards[i]["cardSpecification"].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.workoutCards[i]["cardSpecification"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.workoutCards[i]["cardSpecification"].setFont(inter12)

            self.workoutCards[i]["cardAddButton"] = QPushButton(self)
            self.workoutCards[i]["cardAddButton"].setGeometry(QRect(308 + (i*340), 441, 120, 30))
            self.workoutCards[i]["cardAddButton"].setText("Add to activity")
            self.workoutCards[i]["cardAddButton"].setStyleSheet(f"color: #ffffff; background-color: {DARK_YELLOW}; border: none; border-radius: 12px; font-weight: bold;")
            self.workoutCards[i]["cardAddButton"].clicked.connect(lambda x, i=i: self.addWorkoutCardToActivity(i))
            self.workoutCards[i]["cardAddButton"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.workoutCards[i]["cardTutorialButton"] = QPushButton(self)
            self.workoutCards[i]["cardTutorialButton"].setGeometry(QRect((172) + (i*340), 441, 90, 30))
            self.workoutCards[i]["cardTutorialButton"].setText("Tutorial")
            self.workoutCards[i]["cardTutorialButton"].setStyleSheet("color: #6E7198; background: transparent; border: 2px solid; border-color: #6E7198; border-radius: 12px;")
            self.workoutCards[i]["cardTutorialButton"].clicked.connect(lambda x, i=i: self.openTutorial(i))
            self.workoutCards[i]["cardTutorialButton"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.workoutPlanCards = []
        for i in range(3):
            self.workoutPlanCards.append({})
            self.workoutPlanCards[i]["card"] = QLabel(self)
            self.workoutPlanCards[i]["card"].setPixmap(QPixmap("../img/template-blue-card.png"))
            self.workoutPlanCards[i]["card"].setStyleSheet(f"background-color: {BG_COLOR}")
            self.workoutPlanCards[i]["card"].move(150 + (i%3*340), 568)
            self.workoutPlanCards[i]["cardTitle"] = QLabel(self)
            self.workoutPlanCards[i]["cardTitle"].setText("Title")
            self.workoutPlanCards[i]["cardTitle"].move(172 + (i%3*340), 586)
            self.workoutPlanCards[i]["cardTitle"].setStyleSheet(f"color: {PRIMARY_WHITE}; background-color: {GRAPE}")
            self.workoutPlanCards[i]["cardTitle"].setFont(inter24bold)
            self.workoutPlanCards[i]["cardDescription"] = QLabel(self)
            self.workoutPlanCards[i]["cardDescription"].setText("Desciption")
            self.workoutPlanCards[i]["cardDescription"].move(172 + (i%3*340), 620)
            self.workoutPlanCards[i]["cardDescription"].setStyleSheet(f"color: {PRIMARY_WHITE}; background-color: {GRAPE}")
            self.workoutPlanCards[i]["cardDescription"].setFont(inter12)
            self.workoutPlanCards[i]["cardSeeMoreButton"] = QPushButton(self)
            self.workoutPlanCards[i]["cardSeeMoreButton"].setGeometry(QRect(337 + (i*340), 586, 90, 30))
            self.workoutPlanCards[i]["cardSeeMoreButton"].setText("See More")
            self.workoutPlanCards[i]["cardSeeMoreButton"].setStyleSheet(f"color: {PRIMARY_WHITE}; background-color: {PRIMARY_BUTTON}; border: none; border-radius: 12px; font-weight: bold;")
            self.workoutPlanCards[i]["cardSeeMoreButton"].clicked.connect(lambda x, i=i: self.openWorkoutPlan(i))

    def setUpDisplayWorkout(self):
        if self.listWorkoutPlan == None:
            listWorkout = self.workout
        else:
            # Untuk kasus display workout dalam sebuah workout plan
            listWorkout = self.listWorkoutPlan

        start = self.pageWorkout*3
        for i in range(3):
            if start+i < len(listWorkout):
                self.workoutCards[i]["cardTitle"].setText(listWorkout[start+i]["name"])
                if (listWorkout[start+i]["linkIllustration"][:4] == "http"):
                    pixmap = QPixmap()
                    request = requests.get(listWorkout[start+i]["linkIllustration"])
                    pixmap.loadFromData(request.content)
                    pixmap.scaledToHeight(120)
                    self.workoutCards[i]["cardIllustration"].setPixmap(pixmap.scaledToHeight(120))
                else:
                    self.workoutCards[i]["cardIllustration"].setPixmap(QPixmap(listWorkout[start+i]["linkIllustration"]))
                self.workoutCards[i]["cardDescription"].setText(listWorkout[start+i]["description"])
                self.workoutCards[i]["cardSpecification"].setText(listWorkout[start+i]["specification"])
                self.workoutCards[i]["card"].show()
                self.workoutCards[i]["cardIllustration"].show()
                self.workoutCards[i]["cardTitle"].show()
                self.workoutCards[i]["cardDescription"].show()
                self.workoutCards[i]["cardSpecification"].show()
                self.workoutCards[i]["cardAddButton"].show()
                self.workoutCards[i]["cardTutorialButton"].show()
            else:
                self.workoutCards[i]["card"].hide()
                self.workoutCards[i]["cardIllustration"].hide()
                self.workoutCards[i]["cardTitle"].hide()
                self.workoutCards[i]["cardDescription"].hide()
                self.workoutCards[i]["cardSpecification"].hide()
                self.workoutCards[i]["cardAddButton"].hide()
                self.workoutCards[i]["cardTutorialButton"].hide()

        if self.pageWorkout == 0:
            self.leftWorkoutButton.hide()
        else:
            self.leftWorkoutButton.show()

        if start + 3 < len(listWorkout):
            self.rightWorkoutButton.show()
        else:
            self.rightWorkoutButton.hide()

    def setUpDisplayWorkoutPlan(self):
        startWorkoutPlan = self.pageWorkoutPlan*3
        for i in range(3):
            if startWorkoutPlan+i < len(self.workoutPlan):
                self.workoutPlanCards[i]["cardTitle"].setText(self.workoutPlan[startWorkoutPlan+i]["name"])
                self.workoutPlanCards[i]["cardDescription"].setText(self.workoutPlan[startWorkoutPlan+i]["description"])
                self.workoutPlanCards[i]["card"].show()
                self.workoutPlanCards[i]["cardTitle"].show()
                self.workoutPlanCards[i]["cardDescription"].show()
                self.workoutPlanCards[i]["cardSeeMoreButton"].show()
            else:
                self.workoutPlanCards[i]["card"].hide()
                self.workoutPlanCards[i]["cardTitle"].hide()
                self.workoutPlanCards[i]["cardDescription"].hide()
                self.workoutPlanCards[i]["cardSeeMoreButton"].hide()

        if len(self.workoutPlan) == 0:
            self.noWorkoutPlan.show()
        else:
            self.noWorkoutPlan.hide()

        if self.pageWorkoutPlan == 0:
            self.leftWorkoutPlanButton.hide()
        else:
            self.leftWorkoutPlanButton.show()

        if startWorkoutPlan + 3 < len(self.workoutPlan):
            self.rightWorkoutPlanButton.show()
        else:
            self.rightWorkoutPlanButton.hide()

    def addWorkoutCardToActivity(self, idx):
        idx += self.pageWorkout*3
        # add workout to history
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO workout_history 
                (user_id, olahraga_id, name, specification, date)
            VALUES
                (?, ?, ?, ?, ?)
        """, [self.user["id"], self.workout[idx]["olahraga_id"], self.workout[idx]["name"], self.workout[idx]["specification"], date.today()])
        self.conn.commit()

        # Tunjukkan hasil add to activity berhasil
        self.msgBox = QMessageBox()
        self.msgBox.setText("Successfuly added workout to your history!")
        self.msgBox.setWindowTitle("Successfuly added workout to your history!")
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setStyleSheet("background-color: white")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.exec()


    def openTutorial(self, idx):
        idx += self.pageWorkout*3
        webbrowser.open(self.workout[idx]["linkTutorial"])

    def openWorkoutPlan(self, idx):
        idx += self.pageWorkoutPlan*3
        # change view to page workout plan
        self.headingTop.setText(self.workoutPlan[idx]["name"])
        self.pageWorkout = 0

        listWorkoutPlan = []
        c = self.conn.cursor()
        c.execute("""
            SELECT olahraga_id, name, description, specification, linkIllustration, linkTutorial
            FROM workout NATURAL JOIN list_olahraga
            WHERE request_id = ?
        """, [self.workoutPlan[idx]["id"]])
        temp = c.fetchall()
        c.close()
        for t in temp:
            listWorkoutPlan.append({
                "olahraga_id": t[0],
                "name": t[1],
                "description": t[2],
                "specification": t[3],
                "linkIllustration": t[4],
                "linkTutorial": t[5]
            })
        self.listWorkoutPlan = listWorkoutPlan

        self.headingBottom.hide()
        self.rightWorkoutPlanButton.hide()
        self.leftWorkoutPlanButton.hide()
        for i in range(3):
            self.workoutPlanCards[i]["card"].hide()
            self.workoutPlanCards[i]["cardTitle"].hide()
            self.workoutPlanCards[i]["cardDescription"].hide()
            self.workoutPlanCards[i]["cardSeeMoreButton"].hide()

        self.setUpDisplayWorkout()

    def rightWorkoutButtonClicked(self):
        if self.listWorkoutPlan is not None:
            if self.pageWorkoutPlan < (len(self.workoutPlan)-1)//3:
                self.pageWorkoutPlan += 1
                self.setUpDisplayWorkoutPlan()
        else:
            if self.pageWorkout < (len(self.workout)-1)//3:
                self.pageWorkout += 1
                self.setUpDisplayWorkout()

    def leftWorkoutButtonClicked(self):
        if self.pageWorkout > 0:
            self.pageWorkout -= 1
            self.setUpDisplayWorkout()

    def rightWorkoutPlanButtonClicked(self):
        if self.pageWorkoutPlan + 1 < (len(self.workoutPlan)//3):
            self.pageWorkoutPlan += 1
            self.setUpDisplayWorkoutPlan()

    def leftWorkoutPlanButtonClicked(self):
        if self.pageWorkoutPlan > 0:
            self.pageWorkoutPlan -= 1
            self.setUpDisplayWorkoutPlan()

    def backWP(self):
        self.listWorkoutPlan = None
        self.pageWorkout = 0
        self.headingTop.setText("Workout Activity")
        self.headingBottom.show()
        self.rightWorkoutPlanButton.show()
        self.leftWorkoutPlanButton.show()
        self.setUpDisplayWorkout()
        self.setUpDisplayWorkoutPlan()

    def fetchWorkout(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM list_olahraga")
        workouts = c.fetchall()
        c.close()

        dataWorkout = []
        for workout in workouts:
            dataWorkout.append({
                "olahraga_id": workout[0],
                "name": workout[1],
                "description": workout[2],
                "specification": workout[3],
                "linkIllustration": workout[4],
                "linkTutorial": workout[5]
            })
        self.workout = dataWorkout

    def fetchWorkoutPlan(self, user):
        c = self.conn.cursor()
        c.execute("""
            SELECT request_id, title, description
            FROM daftar_request
            WHERE user_id = ?
        """, [user["id"]])
        workoutPlans = c.fetchall()
        c.close()

        dataWorkoutPlan = []
        for workoutPlan in workoutPlans:
            dataWorkoutPlan.append({
                "id": workoutPlan[0],
                "name": workoutPlan[1],
                "description": workoutPlan[2]
            })
        self.workoutPlan = dataWorkoutPlan
        self.setUpDisplayWorkoutPlan()

    def updateUser(self, user):
        self.user = user
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")

    def back(self):
        if self.listWorkoutPlan is None:
            self.switch.emit("user_dashboard", self.user)
        else:
            self.backWP()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayWorkout()
    window.show()
    sys.exit(app.exec())