import sqlite3
import sys
import requests

from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QTextEdit, QWidget)

from custom_widgets import ClickableLabel

bg_color = '#28293D'
heading2_color = '#7F98BC'
atlantic = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #3eebbe stop:0.0001 #4ec1f3, stop:1 #68fcd6)'
white = "#FFFFFF"
btn_color = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #5561ff, stop:1 #3643fc);'
btn_color_hover = 'qlineargradient(x1:0, y1:0, x2:1, y2: 1, stop:0 #6b75ff, stop:1 #535fff)'

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


class InstructorDashboard(QWidget):
  switch = pyqtSignal(str, dict)

  def __init__(self, user = None):
    super().__init__()
    self.conn = sqlite3.connect("fitpal.db")
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
    self.setWindowTitle("FitPal - Add Workout")
    self.setUpWidgets()
  
  def setUpWidgets(self):
    # Fonts
    inter13 = QFont()
    inter13.setFamily("Inter")
    inter13.setPixelSize(13)

    inter16 = QFont()
    inter16.setFamily("Inter"); 
    inter16.setPixelSize(16)

    inter18 = QFont()
    inter18.setFamily("Inter"); 
    inter18.setPixelSize(18)    

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
    # logoPixmap = QPixmap("../img/dashboard-fitpal-logo.png")
    # logo = QLabel(self)
    # logo.setPixmap(logoPixmap)
    # logo.move(60, 30)
    # logo.setStyleSheet(f"background-color: {bg_color}")
    # Set up hello label
    self.helloLabel = QLabel(self)
    self.helloLabel.setText(f"Hello, {self.user['fullname']}!")
    self.helloLabel.move(635, 44)
    self.helloLabel.setStyleSheet(f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}')
    self.helloLabel.setFixedSize(585, 29)
    self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.helloLabel.setFont(inter24)
    # Set up heading label
    heading = QLabel(self)
    heading.setText("Add Final Course")
    heading.move(60, 40)
    heading.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
    heading.setFont(inter48)
    # Set up heading 2
    heading2 = QLabel(self)
    heading2.setText("Configure your course here")
    heading2.move(60, 100)
    heading2.setStyleSheet(f"color: {heading2_color}; background-color: {bg_color}")
    heading2.setFont(inter24)
    # Set up log out button
    backBtn = QPushButton(self)
    backBtn.setText("Back")
    backBtn.setStyleSheet(f'''
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
    backBtn.setFixedSize(121, 48)
    backBtn.setFont(inter16)
    backBtn.move(1099, 88)
    backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    backBtn.clicked.connect(self.back)
    
    #input title
    title = QLabel(self)
    title.setText("Title")
    title.move(60,140)
    title.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    title.setFont(inter18)
    self.title = QLabel(self)
    self.title.setText("PyQT6")
    self.title.setFixedSize(540, 45)
    self.title.move(60, 170)
    self.title.setStyleSheet('''
      padding: 11px 30px 11px 30px;
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      color: rgba(255, 255, 255, 0.8);
      background-color: #3E405B
    ''')
    self.title.setFont(inter16)
    # self.title = QLineEdit(self)
    # self.title.setPlaceholderText("Insert your course subject!")
    # self.title.setFixedSize(540, 45)
    # self.title.move(60, 170)
    # self.title.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.title.setFont(inter16)

    # Input spec
    specification = QLabel(self)
    specification.setText("Description")
    specification.move(60,230)
    specification.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    specification.setFont(inter18)
    # self.specification = QLineEdit(self)
    # self.specification.setPlaceholderText("Describe your course here!")
    # self.specification.setFixedSize(540, 45)
    # self.specification.move(60, 260)
    # self.specification.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.specification.setFont(inter16)
    self.specification = QLabel(self)
    self.specification.setText("In this course you will learn how to code with pyqt6!")
    self.specification.setFixedSize(540, 45)
    self.specification.move(60, 260)
    self.specification.setStyleSheet('''
      padding: 11px 30px 11px 30px;
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      color: rgba(255, 255, 255, 0.8);
      background-color: #3E405B
    ''')
    self.specification.setFont(inter16)

    # Tutorial = QLabel(self)
    # Tutorial.setText("Tutorial Link")
    # Tutorial.move(60,450)
    # Tutorial.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    # Tutorial.setFont(inter18)
    # self.Tutorial = QLineEdit(self)
    # self.Tutorial.setPlaceholderText("Example: https://bit.ly/someLinkHere")
    # self.Tutorial.setFixedSize(465, 45)
    # self.Tutorial.move(60, 480)
    # self.Tutorial.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.Tutorial.setFont(inter16)

    desc = QLabel(self)
    desc.setText("Final Exam (Case)")
    desc.move(60,330)
    desc.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    desc.setFont(inter18)
    self.desc = QTextEdit(self)
    self.desc.setFixedSize(540, 200)
    self.desc.move(60, 360)
    self.desc.setStyleSheet('''
      padding: 11px 30px 11px 30px;
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      color: rgba(255, 255, 255, 0.8);
      background-color: #3E405B
    ''')
    self.desc.setFont(inter16)

    # answer = QLabel(self)
    # answer.setText("Final Exam (Case)")
    # answer.move(660,330)
    # answer.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    # answer.setFont(inter18)
    # self.answer = QTextEdit(self)
    # self.answer.setFixedSize(540, 200)
    # self.answer.move(60, 360)
    # self.answer.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.desc.setFont(inter16)

    # illustration = QLabel(self)
    # illustration.setText("Illustration Link")
    # illustration.move(660,450)
    # illustration.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    # illustration.setFont(inter18)
    # self.illustration = QLineEdit(self)
    # self.illustration.setPlaceholderText("Example: https://bit.ly/someLinkHere")
    # self.illustration.setFixedSize(465, 45)
    # self.illustration.move(660, 480)
    # self.illustration.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.illustration.setFont(inter16)
    self.initializeAnswerCards()


    self.goBack = QPushButton(self)
    self.goBack.setText("Back")
    self.goBack.setFixedSize(180, 45)
    self.goBack.move(60, 615)
    self.goBack.setStyleSheet(f'''
      QPushButton {{
        color: #ffffff;
        background-color: #F10628;
        border: none;
        border-radius: 12px;
      }}
      QPushButton:hover {{
        background-color: #f43853;
      }}
    ''')
    self.goBack.setFont(inter16)
    self.goBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.goBack.clicked.connect(self.backToDisplayWorkout)

    self.Add = QPushButton(self)
    self.Add.setText("Add")
    self.Add.setFixedSize(180, 45)
    self.Add.move(270, 615)
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

  def initializeAnswerCards(self):
      # Set up font
      inter10 = QFont()
      inter10.setFamily("Inter")
      inter10.setPixelSize(10)

      inter12 = QFont()
      inter12.setFamily("Inter")
      inter12.setPixelSize(12)

      inter18 = QFont()
      inter18.setFamily("Inter"); 
      inter18.setPixelSize(18)    


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
      self.headingTop.setText("Student's Answer")
      self.headingTop.move(660, 120)
      self.headingTop.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
      self.headingTop.setFont(inter18)
      
      # Set up heading Workout Plan label

      # Set up workout cards with empty set
      self.AnswerCards = []
      for i in range(3):
          self.AnswerCards.append({})
          self.AnswerCards[i]["card"] = QLabel(self)
          self.AnswerCards[i]["card"].setGeometry(QRect(660, 220 + (i * 100), 500, 60))
          self.AnswerCards[i]["card"].setStyleSheet(f"background-color: {YELLOW}")
          # self.AnswerCards[i]["card"].setPixmap(QPixmap("../img/template-YELLOW-card.png"))
          # self.AnswerCards[i]["cardIllustration"] = QLabel(self)
          # self.AnswerCards[i]["cardIllustration"].setGeometry(QRect(240 + (i%3*340), 200, 120, 120))
          # self.AnswerCards[i]["cardIllustration"].setStyleSheet(f"background-color: {YELLOW}")
          # self.AnswerCards[i]["cardIllustration"].setPixmap(QPixmap("../img/push-up.png"))
          self.AnswerCards[i]["cardTitle"] = QLabel(self)
          self.AnswerCards[i]["cardTitle"].setGeometry(QRect(670, 235 + (i%3*100), 260, 30))
          self.AnswerCards[i]["cardTitle"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {YELLOW}")
          self.AnswerCards[i]["cardTitle"].setText("Title")
          self.AnswerCards[i]["cardTitle"].setFont(inter16bold)
          # self.AnswerCards[i]["cardDescription"] = QLabel(self)
          # self.AnswerCards[i]["cardDescription"].setText("Description")
          # self.AnswerCards[i]["cardDescription"].setGeometry(QRect(172 + (i%3*340), 366, 256, 64))
          # self.AnswerCards[i]["cardDescription"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
          # self.AnswerCards[i]["cardDescription"].setFont(inter10)
          # self.AnswerCards[i]["cardSpecification"] = QLabel(self)
          # self.AnswerCards[i]["cardSpecification"].setText("Specification")
          # self.AnswerCards[i]["cardSpecification"].setAlignment(Qt.AlignmentFlag.AlignRight)
          # self.AnswerCards[i]["cardSpecification"].setGeometry(QRect(350 + (i*340), 344, 80, 14))
          # self.AnswerCards[i]["cardSpecification"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
          # self.AnswerCards[i]["cardSpecification"].setFont(inter12)

          self.AnswerCards[i]["Input"] = QTextEdit(self)
          self.AnswerCards[i]["Input"].setGeometry(QRect((1065) , 235 + (i*100), 40, 30))
          self.AnswerCards[i]["Input"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
          self.AnswerCards[i]["Input"].setPlaceholderText("Input")
          # self.AnswerCards[i]["Input"].setFont(inter16bold)
          self.AnswerCards[i]["Input"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

          self.AnswerCards[i]["Save"] = QPushButton(self)
          self.AnswerCards[i]["Save"].setGeometry(QRect((1110) , 235 + (i*100), 40, 30))
          self.AnswerCards[i]["Save"].setText("Save")
          self.AnswerCards[i]["Save"].setStyleSheet("color: #6E7198; background: transparent; border: 2px solid; border-color: #6E7198; border-radius: 12px;")
          # self.AnswerCards[i]["Save"].clicked.connect(lambda x, i=i: self.openTutorial(i))
          self.AnswerCards[i]["Save"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

  def setUpDisplayWorkout(self):
      listWorkout = self.workout
      start = self.pageWorkout*3
      for i in range(3):
          if start+i < len(listWorkout):
              self.AnswerCards[i]["cardTitle"].setText(listWorkout[start+i]["name"])
              if (listWorkout[start+i]["linkIllustration"][:4] == "http"):
                  pixmap = QPixmap()
                  request = requests.get(listWorkout[start+i]["linkIllustration"])
                  pixmap.loadFromData(request.content)
                  self.AnswerCards[i]["cardIllustration"].setPixmap(pixmap.scaledToHeight(120))
              else:
                self.AnswerCards[i]["cardIllustration"].setPixmap(QPixmap(listWorkout[start+i]["linkIllustration"]))
                self.AnswerCards[i]["cardDescription"].setText(listWorkout[start+i]["description"])
                self.AnswerCards[i]["cardSpecification"].setText(listWorkout[start+i]["specification"])
                self.AnswerCards[i]["card"].show()
                self.AnswerCards[i]["cardIllustration"].show()
                self.AnswerCards[i]["cardTitle"].show()
                self.AnswerCards[i]["cardDescription"].show()
                self.AnswerCards[i]["cardSpecification"].show()
                self.AnswerCards[i]["Save"].show()
          else:
              self.AnswerCards[i]["card"].hide()
              self.AnswerCards[i]["cardIllustration"].hide()
              self.AnswerCards[i]["cardTitle"].hide()
              self.AnswerCards[i]["cardDescription"].hide()
              self.AnswerCards[i]["cardSpecification"].hide()
              self.AnswerCards[i]["Save"].hide()

      if self.pageWorkout == 0:
          self.leftWorkoutButton.hide()
      else:
          self.leftWorkoutButton.show()

      if start + 3 < len(listWorkout):
          self.rightWorkoutButton.show()
      else:
          self.rightWorkoutButton.hide()

  def addWorkout(self):
    if (self.title.text() == '' or self.specification.text() == '' or self.desc.toPlainText() == '' or self.illustration.text() == '' or self.Tutorial.text() == ''):
      msgBox = QMessageBox()
      msgBox.setText("<p>Please fill out the form properly!</p>")
      msgBox.setWindowTitle("Add New Workout Failed")
      msgBox.setIcon(QMessageBox.Icon.Warning)
      msgBox.setStyleSheet("background-color: white")
      msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
      msgBox.exec()
      return
    c = self.conn.cursor()
    c.execute(f"SELECT * FROM list_olahraga WHERE name = '{self.title.text()}' AND specification = '{self.specification.text()}' AND forUser = 'null'")
    if (c.fetchone() != None):
      msgBox = QMessageBox()
      msgBox.setText("<p>Workout already exists!</p>")
      msgBox.setWindowTitle("Add New Workout Failed")
      msgBox.setIcon(QMessageBox.Icon.Warning)
      msgBox.setStyleSheet("background-color: white")
      msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
      msgBox.exec()
      return
    c.execute(f"INSERT INTO list_olahraga (name, description, specification, linkIllustration, linkTutorial, forUser) VALUES ('{self.title.text()}', '{self.desc.toPlainText()}', '{self.specification.text()}', '{self.illustration.text()}', '{self.Tutorial.text()}', NULL)")
    self.conn.commit()
  # Tunjukkan registrasi berhasil
    msgBox = QMessageBox()
    msgBox.setText(f"<p>Workout has been added successfully!</p>")
    msgBox.setWindowTitle("Add New Workout Successful")
    msgBox.setIcon(QMessageBox.Icon.Information)
    msgBox.setStyleSheet("background-color: white")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgBox.exec()
  # Clear form inputs
    self.title.clear()
    self.specification.clear()
    self.desc.clear()
    self.illustration.clear()
    self.Tutorial.clear()
        
  def backToDisplayWorkout(self):
    self.switch.emit("display_workout", self.user)

  def updateUser(self, user):
    self.user = user
    self.helloLabel.setText(f"Hello, {self.user['fullname']}!")

  def back(self):
    self.switch.emit("login", {})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstructorDashboard()
    window.show()
    sys.exit(app.exec())
