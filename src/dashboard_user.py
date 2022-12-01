import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

bg_color = '#28293D'
atlantic = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
light_yellow = '#FFD9A0'
light_purple = '#A19AFE'
btn_color = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
btn_color_hover = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'


class UserDashboard(QWidget):
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
        self.setUpDashboardWindow()

    def setUpDashboardWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("FitPal - User Dashboard")
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
        heading.setText("What do you want to do?")
        heading.move(60, 120)
        heading.setStyleSheet(
            f"color: {atlantic}; background-color: {bg_color}")
        heading.setFont(inter48)
        # Set up cards
        yellowCard = QLabel(self)
        yellowCardPixmap = QPixmap("../img/dashboard-card-yellow")
        yellowCard.setPixmap(yellowCardPixmap)
        yellowCard.move(60, 195)
        yellowCard.setStyleSheet(f"background-color: {bg_color}")

        purpleCard = QLabel(self)
        purpleCardPixmap = QPixmap("../img/dashboard-card-purple")
        purpleCard.setPixmap(purpleCardPixmap)
        purpleCard.move(490, 195)
        purpleCard.setStyleSheet(f"background-color: {bg_color}")
        # Set up yellow card
        yHeading = QLabel(self)
        yHeading.setText("See available workouts")
        yHeading.setFont(inter24bold)
        yHeading.move(90, 446)
        yHeading.setStyleSheet(
            f"color: rgba(0, 0, 0, 0.5); background-color: {light_yellow}")
        yText = QLabel(self)
        yText.setText(
            "Have no idea on what do you want to do?\nWe got you, fam!")
        yText.setFont(inter13)
        yText.move(90, 477)
        yText.setStyleSheet(
            f"color: rgba(0, 0, 0, 0.5); background-color: {light_yellow}")
        goSeeWorkoutBtn = QPushButton(self)
        goSeeWorkoutBtn.setText("Go!")
        goSeeWorkoutBtn.setStyleSheet(f'''
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
        goSeeWorkoutBtn.setFixedSize(90, 48)
        goSeeWorkoutBtn.setFont(inter16)
        goSeeWorkoutBtn.move(211, 532)
        goSeeWorkoutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        goSeeWorkoutBtn.clicked.connect(self.seeWorkout)
        # Set up purple card
        pHeading = QLabel(self)
        pHeading.setText("See or add workout history")
        pHeading.setFont(inter24bold)
        pHeading.move(520, 446)
        pHeading.setStyleSheet(
            f"color: rgba(0, 0, 0, 0.5); background-color: {light_purple}")
        pText = QLabel(self)
        pText.setText("Want to check out your progress, or add something\nnew to your progress?")
        pText.setFont(inter13)
        pText.move(520, 477)
        pText.setStyleSheet(
            f"color: rgba(0, 0, 0, 0.5); background-color: {light_purple}")
        goCompleteWorkoutBtn = QPushButton(self)
        goCompleteWorkoutBtn.setText("Go!")
        goCompleteWorkoutBtn.setStyleSheet(f'''
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
        goCompleteWorkoutBtn.setFixedSize(90, 48)
        goCompleteWorkoutBtn.setFont(inter16)
        goCompleteWorkoutBtn.move(654, 532)
        goCompleteWorkoutBtn.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        goCompleteWorkoutBtn.clicked.connect(self.finish_workout)
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

    def updateUser(self, user):
        self.user = user
        self.helloLabel.setText(f"Hello, {self.user['fullname']}!")

    def finish_workout(self):
        self.switch.emit("finish_workout", self.user)

    def logOut(self):
        self.switch.emit("login", {})

    def seeWorkout(self):
        self.switch.emit("display_workout", self.user)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserDashboard()
    window.show()
    sys.exit(app.exec())
