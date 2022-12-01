import sqlite3
import sys
import webbrowser

import requests
from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

bg_color = '#28293D'
primary_black = '#000000'
primary_white = '#FFFFFF'
primary_button = '#5561FF'
yellow = '#FEC166'
dark_yellow = '#EEA02B'
grape = '#7366FE'
atlantic = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
light_yellow = '#FFD9A0'
primary_red = '#F10628'
primary_red_hover = "#f43853"
btn_color = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
btn_color_hover = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'
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

class DisplayWorkoutTrainer(QWidget):
    switch = pyqtSignal(str, dict)

    def __init__(self, user = None):
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
        self.conn = sqlite3.connect('fitpal.db')
        self.pageWorkout = 0
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
        self.setStyleSheet(f"background-color: {bg_color}")

        # Set up logo
        logoPixmap = QPixmap("../img/dashboard-fitpal-logo.png")
        logo = QLabel(self)
        logo.setPixmap(logoPixmap)
        logo.move(60, 30)
        logo.setStyleSheet(f"background-color: {bg_color}")

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

        self.backBtn = QPushButton(self)
        self.backBtn.setText("Back")
        self.backBtn.setStyleSheet(back_btn_style)
        self.backBtn.setFont(inter16)
        self.backBtn.setFixedSize(121, 45)
        self.backBtn.move(60, 615)
        self.backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.backBtn.clicked.connect(self.trainerDashboard)

        self.Add = QPushButton(self)
        self.Add.setText("Add new workout")
        self.Add.setFixedSize(189, 45)
        self.Add.move(190, 615)
        self.Add.setStyleSheet('''
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
        self.Add.setFont(inter16)
        self.Add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Add.clicked.connect(self.addWorkout)

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
        self.headingTop.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
        self.headingTop.setFont(inter48)
        
        # Set up heading Workout Plan label

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
            self.workoutCards[i]["cardSpecification"].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.workoutCards[i]["cardSpecification"].setGeometry(QRect(350 + (i*340), 344, 80, 14))
            self.workoutCards[i]["cardSpecification"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.workoutCards[i]["cardSpecification"].setFont(inter12)

            self.workoutCards[i]["cardTutorialButton"] = QPushButton(self)
            self.workoutCards[i]["cardTutorialButton"].setGeometry(QRect((172) + (i*340), 441, 90, 30))
            self.workoutCards[i]["cardTutorialButton"].setText("Tutorial")
            self.workoutCards[i]["cardTutorialButton"].setStyleSheet("color: #6E7198; background: transparent; border: 2px solid; border-color: #6E7198; border-radius: 12px;")
            self.workoutCards[i]["cardTutorialButton"].clicked.connect(lambda x, i=i: self.openTutorial(i))
            self.workoutCards[i]["cardTutorialButton"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setUpDisplayWorkout(self):
        listWorkout = self.workout
        start = self.pageWorkout*3
        for i in range(3):
            if start+i < len(listWorkout):
                self.workoutCards[i]["cardTitle"].setText(listWorkout[start+i]["name"])
                if (listWorkout[start+i]["linkIllustration"][:4] == "http"):
                    pixmap = QPixmap()
                    request = requests.get(listWorkout[start+i]["linkIllustration"])
                    pixmap.loadFromData(request.content)
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
                self.workoutCards[i]["cardTutorialButton"].show()
            else:
                self.workoutCards[i]["card"].hide()
                self.workoutCards[i]["cardIllustration"].hide()
                self.workoutCards[i]["cardTitle"].hide()
                self.workoutCards[i]["cardDescription"].hide()
                self.workoutCards[i]["cardSpecification"].hide()
                self.workoutCards[i]["cardTutorialButton"].hide()

        if self.pageWorkout == 0:
            self.leftWorkoutButton.hide()
        else:
            self.leftWorkoutButton.show()

        if start + 3 < len(listWorkout):
            self.rightWorkoutButton.show()
        else:
            self.rightWorkoutButton.hide()

    def openTutorial(self, idx):
        idx += self.pageWorkout*3
        webbrowser.open(self.workout[idx]["linkTutorial"])
    
    def rightWorkoutButtonClicked(self):
        if (self.pageWorkout < (len(self.workout)//3)):
            self.pageWorkout += 1
            self.setUpDisplayWorkout()

    def leftWorkoutButtonClicked(self):
        if (self.pageWorkout > 0):
            self.pageWorkout -= 1
            self.setUpDisplayWorkout()
    
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
    
    def updateUser(self, user):
        self.user = user
    
    def trainerDashboard(self):
        self.switch.emit("trainer_dashboard", self.user)
    
    def logOut(self):
        self.switch.emit("login", {})

    def addWorkout(self):
        self.switch.emit("add_workout", self.user)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayWorkoutTrainer()
    window.show()
    sys.exit(app.exec())
