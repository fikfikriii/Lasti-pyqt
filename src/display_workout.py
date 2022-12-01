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
    switch = pyqtSignal(str, dict, dict)

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
        self.conn = sqlite3.connect('course.db')
        self.pageCourses = 0
        self.pageCoursesPlan = 0
        self.coursesPlan = []
        self.listCoursesPlan = None
        self.fetchCourses()
        self.setUpDisplayCoursesWindow()

    def updateDisplayCourses(self):
        self.fetchCourses()
        self.setUpDisplayCourses()

    def setUpDisplayCoursesWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Udemy - Display Courses")
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
        logoPixmap = QPixmap("../img/logo-udemy-dashboard.png")
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

        # Set up logout button
        logoutBtn = QPushButton(self)
        logoutBtn.setText("Logout")
        logoutBtn.setStyleSheet(f'''
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
        logoutBtn.setFixedSize(121, 48)
        logoutBtn.setFont(inter16)
        logoutBtn.move(1099, 88)
        logoutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logoutBtn.clicked.connect(self.logout)

        self.rightCoursesButton = QPushButton(self)
        self.rightCoursesButton.setGeometry(QRect(1130, 308, 48, 48))
        self.rightCoursesButton.setStyleSheet("background-image: url(../img/right-btn.png);")
        self.rightCoursesButton.clicked.connect(self.rightCoursesButtonClicked)
        self.rightCoursesButton.hide()
        self.rightCoursesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.leftCoursesButton = QPushButton(self)
        self.leftCoursesButton.setGeometry(QRect(102, 308, 48, 48))
        self.leftCoursesButton.setStyleSheet("background-image: url(../img/left-btn.png);")
        self.leftCoursesButton.clicked.connect(self.leftCoursesButtonClicked)
        self.leftCoursesButton.hide()
        self.leftCoursesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        # Set up courses cards from courses
        self.initializeCoursesCards()
        self.setUpDisplayCourses()

    def initializeCoursesCards(self):
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
        
        inter16 = QFont()
        inter16.setFamily("Inter")
        inter16.setPixelSize(16)

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
        self.headingTop.setText("My Courses")
        self.headingTop.move(60, 130)
        self.headingTop.setStyleSheet(f"color: {ATLANTIC}; background-color: {BG_COLOR}")
        self.headingTop.setFont(inter48)

        # Set up workout cards with empty set
        self.coursesCards = []
        for i in range(3):
            self.coursesCards.append({})
            self.coursesCards[i]["card"] = QLabel(self)
            self.coursesCards[i]["card"].setGeometry(QRect(150 + (i * 340), 250, 300, 300))
            self.coursesCards[i]["card"].setStyleSheet(f"background-color: {BG_COLOR}")
            self.coursesCards[i]["card"].setPixmap(QPixmap("../img/template-YELLOW-card.png"))
            
            self.coursesCards[i]["cardIllustration"] = QLabel(self)
            self.coursesCards[i]["cardIllustration"].setGeometry(QRect(240 + (i%3*340), 262, 120, 120))
            self.coursesCards[i]["cardIllustration"].setStyleSheet(f"background-color: {YELLOW}")
            self.coursesCards[i]["cardIllustration"].setPixmap(QPixmap(f"../img/display-student-{i+1}.png"))
            
            self.coursesCards[i]["cardTitle"] = QLabel(self)
            self.coursesCards[i]["cardTitle"].setGeometry(QRect(172 + (i%3*340), 401, 120, 20))
            self.coursesCards[i]["cardTitle"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.coursesCards[i]["cardTitle"].setText("Title")
            self.coursesCards[i]["cardTitle"].setFont(inter24bold)
            
            self.coursesCards[i]["cardDescription"] = QLabel(self)
            self.coursesCards[i]["cardDescription"].setText("Description")
            self.coursesCards[i]["cardDescription"].setGeometry(QRect(172 + (i%3*340), 428, 256, 64))
            self.coursesCards[i]["cardDescription"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
            self.coursesCards[i]["cardDescription"].setFont(inter16)

            self.coursesCards[i]["openCourseButton"] = QPushButton(self)
            self.coursesCards[i]["openCourseButton"].setGeometry(QRect((172) + (i*340), 503, 90, 30))
            self.coursesCards[i]["openCourseButton"].setText("Open Course")
            self.coursesCards[i]["openCourseButton"].setStyleSheet("color: #6E7198; background: transparent; border: 2px solid; border-color: #6E7198; border-radius: 12px;")
            self.coursesCards[i]["openCourseButton"].clicked.connect(lambda x, i=i: self.openCourse(i))
            self.coursesCards[i]["openCourseButton"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


    def setUpDisplayCourses(self):
        listCoursesPlan = self.course
        start = self.pageCourses*3
        for i in range(3):
            if start+i < len(listCoursesPlan):
                self.coursesCards[i]["cardTitle"].setText(listCoursesPlan[start+i]["name"])
                self.coursesCards[i]["cardDescription"].setText(listCoursesPlan[start+i]["description"])
                self.coursesCards[i]["card"].show()
                self.coursesCards[i]["cardTitle"].show()
                self.coursesCards[i]["cardDescription"].show()
                self.coursesCards[i]["openCourseButton"].show()
            else:
                self.coursesCards[i]["card"].hide()
                self.coursesCards[i]["cardTitle"].hide()
                self.coursesCards[i]["cardIllustration"].hide()
                self.coursesCards[i]["cardDescription"].hide()
                self.coursesCards[i]["openCourseButton"].hide()

        if self.pageCourses == 0:
            self.leftCoursesButton.hide()
        else:
            self.leftCoursesButton.show()

        if start + 3 < len(listCoursesPlan):
            self.rightCoursesButton.show()
        else:
            self.rightCoursesButton.hide()

    def rightCoursesButtonClicked(self):
        if self.listCoursesPlan is not None:
            if self.pageCoursesPlan < (len(self.coursesPlan)-1)//3:
                self.pageCoursesPlan += 1
                self.setUpDisplayCoursesPlan()
        else:
            if self.pageCourses < (len(self.workout)-1)//3:
                self.pageCourses += 1
                self.setUpDisplayCourses()

    def leftCoursesButtonClicked(self):
        if self.pageCourses > 0:
            self.pageCourses -= 1
            self.setUpDisplayCourses()

    def backWP(self):
        self.listCoursesPlan = None
        self.pageCourses = 0
        self.headingTop.setText("Courses Activity")
        self.headingBottom.show()
        self.setUpDisplayCourses()

    def fetchCourses(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM course")
        courses = c.fetchall()
        c.close()

        dataCourses = []
        for course in courses:
            dataCourses.append({
                "course_id": course[0],
                "name": course[1],
                "description": course[2],
                "cost": course[3],
                "owner_id": course[4]
            })
        self.course = dataCourses


    def updateUser(self, user):
        self.user = user
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")

    def logout(self):
        print("logout")
        self.switch.emit("login", {}, {})
        print("te")
    
    def openCourse(self, i):
        self.switch.emit("display_course_student", self.user, self.course[i])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayWorkout()
    window.show()
    sys.exit(app.exec())