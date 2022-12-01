import sqlite3
import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QTextEdit, QWidget)

from custom_widgets import ClickableLabel
from display_workout import DisplayWorkout

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
    self.conn = sqlite3.connect("course.db")
    self.conn2 = sqlite3.connect("final_project.db")
    if (user != None):
      self.user = user
    else:
      self.user = {
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
        "deskripsi": "Ini adalah contoh dari course di Udemy",
        "cost": 10,
        "owner_id": 1
      }
    self.fetchCourse()
    self.fetchFinalProject()
    self.setUpDashboardWindow()
    self.displayWorkout = DisplayWorkout()
    
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
    self.helloLabel = QLabel(self)
    self.helloLabel.setText(f"Hello, {self.user['name']}!")
    self.helloLabel.move(635, 44)
    self.helloLabel.setStyleSheet(f'color: rgba(255, 255, 255, 0.8); background-color: {bg_color}')
    self.helloLabel.setFixedSize(585, 29)
    self.helloLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.helloLabel.setFont(inter24)
    # Set up heading label
    heading = QLabel(self)
    heading.setText(self.course["name"])
    heading.move(60, 40)
    heading.setStyleSheet(f"color: {atlantic}; background-color: {bg_color}")
    heading.setFont(inter48)
    # Set up log out button
    logOutBtn = QPushButton(self)
    logOutBtn.setText("Back")
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

    # Input spec
    specification = QLabel(self)
    specification.setText("Description")
    specification.move(60,120)
    specification.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    specification.setFont(inter18)

    self.isi_deskripsi = QLabel(self)
    self.isi_deskripsi.setText(self.course["description"])
    self.isi_deskripsi.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.isi_deskripsi.move(60,150)
    self.isi_deskripsi.setFixedWidth(300)
    self.isi_deskripsi.setFont(inter16)


    # self.specification.setFont(inter16)
    # self.specification = QLineEdit(self)
    # self.specification.setPlaceholderText("Describe your course here!")
    # self.specification.setFixedSize(540, 45)
    # self.specification.move(60, 150)
    # self.specification.setStyleSheet('''
    #   padding: 11px 30px 11px 30px;
    #   border: 1px solid rgba(255, 255, 255, 0.8);
    #   border-radius: 20px;
    #   color: rgba(255, 255, 255, 0.8);
    #   background-color: #3E405B
    # ''')
    # self.specification.setFont(inter16)

    self.desc = QLabel(self)
    self.desc.setText("Final Exam (Case)")
    self.desc.move(60,330)
    self.desc.setStyleSheet(f"color: {white}; background-color: {bg_color}")
    self.desc.setFont(inter18)



    self.question = QLabel(self)
    self.question.setText(self.final_project["question"])
    self.question.setFixedSize(540, 200)
    self.question.move(60, 360)
    self.question.setStyleSheet('''
      padding: 11px 30px 11px 30px;
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 20px;
      color: rgba(255, 255, 255, 0.8);
      background-color: #3E405B
    ''')
    self.question.setWordWrap(True)
    self.question.setFont(inter18)

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

  def fetchFinalProject(self):
    c = self.conn2.cursor()
    c.execute("SELECT * FROM final_project where final_project_id = 1")
    final_project = c.fetchone()
    c.close()

    dataFinalProject = {"final_project_id" : final_project[0], "name" : final_project[1], "course_id" : final_project[2], "question" : final_project[3]}

    self.final_project = dataFinalProject

  def fetchCourse(self):
    c = self.conn.cursor()
    c.execute("SELECT * FROM course where course_id = 1")
    course = c.fetchone()
    c.close()

    dataCourse = {"course_id" : course[0], "name" : course[1], "description" : course[2], "cost" : course[3], "owner_id" : course[4]}

    self.course = dataCourse

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
    self.helloLabel.setText(f"Hello, {self.user['name']}!")

  def updateCourse(self, course):
    self.course = course

  def logOut(self):
    self.switch.emit("display_workout", self.user)
    self.displayWorkout.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayCourseStudent()
    window.show()
    sys.exit(app.exec())
