import sqlite3
import sys

from PyQt6.QtCore import Qt, pyqtSignal
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

class DisplayCourseStudent(QWidget):
  switch = pyqtSignal(str, dict)

  def __init__(self, user = None, course = None):
    super().__init__()
    self.connCourse = sqlite3.connect("course.db")
    self.connFinalProject = sqlite3.connect("final_project.db")
    self.connFinalProjectAnswer = sqlite3.connect("final_project_answer.db")
    if (user != None):
      self.user = user
    else:
      self.user = {
        "user_id" : 1,
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
    # self.fetchCourse()
    self.fetchFinalProject()
    self.setUpDashboardWindow()
    
  def setUpDashboardWindow(self):
    self.setFixedSize(1280, 720)
    self.setWindowTitle("Udemy " + self.course['name'])
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
    self.helloLabel = QLabel(self)
    self.helloLabel.setText(f"Hello, {self.user['name']}!")
    self.helloLabel.move(635, 44)
    self.helloLabel.setStyleSheet(f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}')
    self.helloLabel.setFixedSize(585, 29)
    self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.helloLabel.setFont(inter24)
    
    # Set up heading label
    self.heading = QLabel(self)
    self.heading.setText(self.course["name"])
    self.heading.move(60, 40)
    self.heading.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
    self.heading.setFont(inter48)
    
    # Set up log out button
    self.logOutBtn = QPushButton(self)
    self.logOutBtn.setText("Back")
    self.logOutBtn.setStyleSheet(f'''
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
    self.logOutBtn.setFixedSize(121, 48)
    self.logOutBtn.setFont(inter16)
    self.logOutBtn.move(1099, 88)
    self.logOutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.logOutBtn.clicked.connect(self.logOut)

    # Input spec
    self.specification_heading = QLabel(self)
    self.specification_heading.setText("Description")
    self.specification_heading.move(60,120)
    self.specification_heading.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.specification_heading.setFont(inter18)

    self.isi_deskripsi = QLabel(self)
    self.isi_deskripsi.setText(self.course["description"])
    self.isi_deskripsi.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.isi_deskripsi.move(60,150)
    self.isi_deskripsi.setFixedWidth(500)
    self.isi_deskripsi.setFont(inter16)
    self.isi_deskripsi.setWordWrap(True)

    self.question_heading = QLabel(self)
    self.question_heading.setText("Final Exam (Case)")
    self.question_heading.move(60,300)
    self.question_heading.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.question_heading.setFont(inter18)
    
    self.question = QLabel(self)
    self.question.setText(self.final_project["question"])
    self.question.setFixedWidth(500)
    self.question.move(60, 330)
    self.question.setStyleSheet('''
      color: rgba(255, 255, 255, 0.8);
    ''')
    self.question.setWordWrap(True)
    self.question.setFont(inter16)

    self.answer_heading = QLabel(self)
    self.answer_heading.setText("Answer Final Project Here")
    self.answer_heading.move(660,300)
    self.answer_heading.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.answer_heading.setFont(inter18)
    self.answer = QTextEdit(self)
    self.answer.setFixedSize(540, 250)
    self.answer.move(660, 330)
    self.answer.setStyleSheet('''
      padding: 11px 30px 11px 30px;
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      color: rgba(255, 255, 255, 0.8);
      background-color: #3E405B
    ''')
    self.answer.setFont(inter16)

    self.Submit = QPushButton(self)
    self.Submit.setText("Submit Answer")
    self.Submit.setFixedSize(180, 45)
    self.Submit.move(1020, 615)
    self.Submit.setStyleSheet('''
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
    self.Submit.setFont(inter16)
    self.Submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.Submit.clicked.connect(self.submitAnswer)

  def fetchFinalProject(self):
    c = self.connFinalProject.cursor()
    c.execute("SELECT * FROM final_project where final_project_id = 1")
    final_project = c.fetchone()
    c.close()

    dataFinalProject = {"final_project_id" : final_project[0], "name" : final_project[1], "course_id" : final_project[2], "question" : final_project[3]}

    self.final_project = dataFinalProject

  def submitAnswer(self):
    if (self.answer.toPlainText() == ''):
      msgBox = QMessageBox()
      msgBox.setText("<p>Please fill out the answer!</p>")
      msgBox.setWindowTitle("Submit Answer Failed")
      msgBox.setIcon(QMessageBox.Icon.Warning)
      msgBox.setStyleSheet("background-color: white")
      msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
      msgBox.exec()
      return
    c = self.connFinalProjectAnswer.cursor()
    c.execute(f'SELECT answer FROM final_project_answer WHERE user_id = {self.user["user_id"]}')
    print(c)
    if (c == None):
      c.execute(f"INSERT INTO final_project_answer(course_id, final_project_id, user_id, answer) VALUES ('{self.course['course_id']}','{self.final_project['final_project_id']}', '{self.user['user_id']}', '{self.answer.toPlainText()}')")
    else:
      c.execute(f"UPDATE final_project_answer SET answer = '{self.answer.toPlainText()}' WHERE user_id = {self.user['user_id']}")
      
    self.connFinalProjectAnswer.commit()
    msgBox = QMessageBox()
    msgBox.setText(f"<p>Answer has been submitted successfully!</p>")
    msgBox.setWindowTitle("Submit Answer Successful")
    msgBox.setIcon(QMessageBox.Icon.Information)
    msgBox.setStyleSheet("background-color: white")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgBox.exec()
    
  def updateUser(self, user):
    self.user = user
    self.helloLabel.setText(f"Hello, {self.user['name']}!")

  def updateCourse(self, course):
    self.course = course
    self.heading.setText(self.course["name"])
    self.isi_deskripsi.setText(self.course["description"])
    self.updateFinalProject()

  def updateFinalProject(self):
    c = self.connFinalProject.cursor()
    c.execute("""
              SELECT * FROM final_project where final_project_id = ?
    """, [self.course["course_id"]])
    res = c.fetchone()
    self.final_project["id"] = res[0]
    self.final_project["name"] = res[1]
    self.final_project["course_id"] = res[2]
    self.final_project["question"] = res[3]    
    self.question.setText(self.final_project["question"])
        
  def logOut(self):
    self.switch.emit("user_course", self.user)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayCourseStudent()
    window.show()
    sys.exit(app.exec())
