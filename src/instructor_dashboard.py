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

  def __init__(self, instructor = None, course = None):
    super().__init__()
    self.connCourse = sqlite3.connect("course.db")
    self.connFinalProject = sqlite3.connect("final_project.db")
    self.connFinalProjectAnswer = sqlite3.connect("final_project_answer.db")
    if (instructor != None):
      self.instructor = instructor
    else:
      self.instructor = {
        "name": "John Doe",
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "password": "johndoe",
      }
      if (course != None):
          self.course = course
      else:
        self.course = {
          "course_id": 1,
          "name": "Contoh course",
          "description": "Ini adalah contoh dari course di Udemy",
          "cost": 10,
          "owner_id": 1
      }
    self.final_project = {
      "final_project_id": 1,
      "course_id": 1,
      "name": "Ini adalah final project",
      "question": "Ini adalah soal final project"
    }
    self.answer = {
      "final_project_id": 1,
      "course_id": 1,
      "user_id": 1,
      "answer": "Ini adalah soal final project",
      "score": 80
    }
    self.fetchFinalProject()
    self.fetchAnswer()
    self.setUpDashboardWindow()

  def setUpDashboardWindow(self):
    self.setFixedSize(1280, 720)
    self.setWindowTitle("Udemy - Edit Final Project")
    self.setUpWidgets()
  
  def setUpWidgets(self):
    # Fonts
    self.inter10bold = QFont()
    self.inter10bold.setFamily("Inter")
    self.inter10bold.setPixelSize(10)
    self.inter10bold.setBold(True)
    
    inter10 = QFont()
    inter10.setFamily("Inter")
    inter10.setPixelSize(10)

    self.inter11bold = QFont()
    self.inter11bold.setFamily("Inter")
    self.inter11bold.setPixelSize(11)
    self.inter11bold.setBold(True)
    
    inter12 = QFont()
    inter12.setFamily("Inter")
    inter12.setPixelSize(12)

    inter16 = QFont()
    inter16.setFamily("Inter") 
    inter16.setPixelSize(16)

    inter18 = QFont()
    inter18.setFamily("Inter") 
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
    # logoPixmap = QPixmap("../img/logo.png")
    # logo = QLabel(self)
    # logo.setPixmap(logoPixmap)
    # logo.move(60, 30)
    # logo.setStyleSheet(f"background-color: {bg_color}")
    # Set up hello label
    self.helloLabel = QLabel(self)
    self.helloLabel.setText(f"Hello, {self.instructor['name']}!")
    self.helloLabel.move(635, 44)
    self.helloLabel.setStyleSheet(f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}')
    self.helloLabel.setFixedSize(585, 29)
    self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.helloLabel.setFont(inter24)
    # Set up heading label
    heading = QLabel(self)
    heading.setText("Edit Course")
    heading.move(60, 40)
    heading.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
    heading.setFont(inter48)
    # Set up heading 2
    heading2 = QLabel(self)
    heading2.setText("Configure your course here")
    heading2.move(60, 100)
    heading2.setStyleSheet(f"color: {heading2_color}; background-color: {bg_color}")
    heading2.setFont(inter24)
    # Set up back button
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
    backBtn.move(60, 615)
    backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    backBtn.clicked.connect(self.back)
    
    # Set up save button
    saveBtn = QPushButton(self)
    saveBtn.setText("Save")
    saveBtn.setStyleSheet(f'''
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
    saveBtn.setFixedSize(121, 48)
    saveBtn.setFont(inter16)
    saveBtn.move(195, 615)
    saveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    saveBtn.clicked.connect(self.addFinalProject)
    
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

    # input spec
    specification = QLabel(self)
    specification.setText("Description")
    specification.move(60,230)
    specification.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    specification.setFont(inter18)

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
    
    finalproject = self.final_project
    desc = QLabel(self)
    desc.setText("Final Exam (Case)")
    desc.move(60,330)
    desc.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    desc.setFont(inter18)
    self.desc = QTextEdit(self)
    self.desc.setPlaceholderText(str(finalproject["question"]))
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

    self.initializeAnswerCards()
    self.setUpDisplayAnswer()

  def fetchFinalProject(self):
    c = self.connFinalProject.cursor()
    c.execute("SELECT * FROM final_project where final_project_id = 1")
    final_project = c.fetchone()
    c.close()

    dataFinalProject = {"final_project_id" : final_project[0], "name" : final_project[1], "course_id" : final_project[2], "question" : final_project[3]}

    self.final_project = dataFinalProject
    
  def fetchAnswer(self):
        c = self.connFinalProjectAnswer.cursor()
        c.execute("""
          SELECT * FROM final_project_answer WHERE course_id = 1
        """)
        answers = c.fetchall()
        c.close()

        dataAnswer = []
        for answer in answers:
            dataAnswer.append({
              "course_id": answer[0],
              "final_project_id": answer[1],
              "user_id": answer[2],
              "answer": answer[3],
              "score": answer[4]
            })
        self.answer = dataAnswer
        
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
          self.AnswerCards[i]["cardTitle"] = QLabel(self)
          self.AnswerCards[i]["cardTitle"].setGeometry(QRect(670, 227 + (i%3*100), 260, 10))
          self.AnswerCards[i]["cardTitle"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: rgba(254, 193, 102, 0)")
          self.AnswerCards[i]["cardTitle"].setText("Title")
          self.AnswerCards[i]["cardTitle"].setFont(self.inter11bold)
          
          self.AnswerCards[i]["cardAnswer"] = QLabel(self)
          self.AnswerCards[i]["cardAnswer"].setGeometry(QRect(670, 255 + (i%3*100), 260, 10))
          self.AnswerCards[i]["cardAnswer"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: rgba(254, 193, 102, 0)")
          self.AnswerCards[i]["cardAnswer"].setText("Answer")
          self.AnswerCards[i]["cardAnswer"].setFont(inter12)

          self.AnswerCards[i]["input"] = QTextEdit(self)
          self.AnswerCards[i]["input"].setGeometry(QRect((1065) , 235 + (i*100), 40, 30))
          self.AnswerCards[i]["input"].setStyleSheet(f"color: {PRIMARY_BLACK}; background-color: {LIGHT_YELLOW}")
          self.AnswerCards[i]["input"].setPlaceholderText("Input")
          # self.AnswerCards[i]["input"].setFont(inter16bold)
          self.AnswerCards[i]["input"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
          

          self.AnswerCards[i]["save"] = QPushButton(self)
          self.AnswerCards[i]["save"].setGeometry(QRect((1110) , 235 + (i*100), 40, 30))
          self.AnswerCards[i]["save"].setText("Save")
          self.AnswerCards[i]["save"].setStyleSheet("color: #6E7198; background: transparent; border: 2px solid; border-color: #6E7198; border-radius: 12px;")
          # self.AnswerCards[i]["save"].clicked.connect(lambda x, i=i: self.openTutorial(i))
          self.AnswerCards[i]["save"].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
          self.AnswerCards[i]["save"].clicked.connect(lambda x, i=i: self.addAnswer(i+1))
          
  
  def addAnswer(self, i):
    score = self.AnswerCards[i-1]["input"].toPlainText()
    c = self.connFinalProjectAnswer.cursor()
    queryAnswer = (f"UPDATE final_project_answer set score = '{score}' WHERE user_id = '{i}'")
    c.execute(queryAnswer)

    self.connFinalProjectAnswer.commit()
    answers = c.fetchall()
    c.close()

    dataAnswer = []
    for answer in answers:
        dataAnswer.append({
          "course_id": answer[0],
          "final_project_id": answer[1],
          "user_id": answer[2],
          "answer": answer[3],
          "score": answer[4]
        })
    self.answer = dataAnswer

  def addFinalProject(self):
    question = self.desc.toPlainText()
    c = self.connFinalProject.cursor()
    queryAnswer = (f"UPDATE final_project set question = '{question}' WHERE final_project_id = 1")
    c.execute(queryAnswer)
    self.connFinalProject.commit()
    c.close()
    

  def setUpDisplayAnswer(self):
      listAnswer = self.answer
      for i in range(3):
          if i < len(listAnswer):
              self.AnswerCards[i]["cardTitle"].setText("User ID: " + str(listAnswer[i]["user_id"]))
              self.AnswerCards[i]["cardAnswer"].setText(listAnswer[i]["answer"])
              self.AnswerCards[i]["input"].setPlaceholderText(str(listAnswer[i]["score"]))
              self.AnswerCards[i]["cardTitle"].show()
              self.AnswerCards[i]["cardAnswer"].show()
              self.AnswerCards[i]["input"].show()
          else:
              self.AnswerCards[i]["cardTitle"].hide()
              self.AnswerCards[i]["cardAnswer"].hide()

      # if self.pageWorkout == 0:
      #     self.leftWorkoutButton.hide()
      # else:
      #     self.leftWorkoutButton.show()

      # if start + 3 < len(listAnswer):
      #     self.rightWorkoutButton.show()
      # else:
      #     self.rightWorkoutButton.hide()

  def updateCourse(self, course):
    self.course = course
    self.title.setText(self.course["name"])
    self.specification.setText(self.course["description"])
    
  def updateUser(self, instructor):
    self.instructor = instructor
    self.helloLabel.setText(f"Hello, {self.instructor['name']}!")

  def back(self):
    self.switch.emit("instructor_course", self.instructor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstructorDashboard()
    window.show()
    sys.exit(app.exec())
