import os.path
import sqlite3
import sys
from tkinter import E

from PyQt6.QtWidgets import QApplication

from dashboard_trainer import TrainerDashboard
from display_workout import DisplayWorkout
from display_workout_trainer import DisplayWorkoutTrainer
from login_window import LoginWindow
from register_window import RegisterWindow
from display_course_student import DisplayCourseStudent

class Controller:
    def __init__(self):
        self.initializeDatabase()
        self.loginWindow = LoginWindow()
        self.loginWindow.switch.connect(self.fromLogin)
        self.registerWindow = RegisterWindow()
        self.registerWindow.switch.connect(self.fromRegister)
        self.displayWorkout = DisplayWorkout()
        self.displayWorkout.switch.connect(self.fromDisplayWorkout)
        self.displayWorkoutTrainer = DisplayWorkoutTrainer()
        self.displayWorkoutTrainer.switch.connect(self.fromDisplayWorkoutTrainer)
        self.displayCourseStudent = DisplayCourseStudent()
        self.displayCourseStudent.switch.connect(self.fromDisplayCourseStudent)
        # self.trainerAddWorkout.connect(self.from)
        pass

    def start(self):
        self.loginWindow.show()

    def fromRegister(self):
        self.registerWindow.close()
        self.loginWindow.clearForm()
        self.loginWindow.show()

    def fromLogin(self, page, user):
        self.loginWindow.close()
        if page == "register":
            self.registerWindow.show()
        elif page == "display_workout":
            self.displayWorkout.show()
        elif page == "dashboard_instructor":
            self.trainerDashboard.updateUser(user)
            self.trainerDashboard.show()        

    def fromDisplayWorkout(self, page, user, course):
        self.displayWorkout.close()
        if page == "login":
            self.loginWindow.clearForm()
            self.loginWindow.show()
        elif page == "display_course_student":
            self.displayCourseStudent.updateCourse(course)
            self.displayCourseStudent.show()

    def fromDisplayWorkoutTrainer(self, page, user):
        self.displayWorkoutTrainer.close()
        if page == "login":
            self.loginWindow.clearForm()
            self.loginWindow.show()
        elif page == "trainer_dashboard":
            self.trainerDashboard.updateUser(user)
            self.trainerDashboard.show()
        
    def fromDisplayCourseStudent(self, page, user):
        self.displayCourseStudent.close()
        if page == 'display_workout':
            self.displayWorkoutTrainer.updateUser(user)
            self.displayWorkoutTrainer.updateDisplayWorkout()
            self.displayWorkoutTrainer.show()

    
    def initializeDatabase(self):
        if not os.path.exists("user.db"):
            self.conn = sqlite3.connect("user.db")
            c = self.conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS user (
                user_id integer PRIMARY KEY,
                name text,
                username text,
                email text,
                password text,
                enrolled_course integer )
            """)
        
        if not os.path.exists("instructor.db"):
            self.conn = sqlite3.connect("instructor.db")
            c = self.conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS instructor (
                instructor_id integer PRIMARY KEY,
                name text,
                username text,
                email text,
                password text )
            """)
        
        if not os.path.exists("course.db"):
            self.conn = sqlite3.connect("course.db")
            c = self.conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS course (
            course_id integer PRIMARY KEY,
            name text,
            description text,
            cost numeric,
            owner_id integer
            )
            """) 
            c.execute("""
            INSERT INTO course
                (course_id, name, description, cost, owner_id)
            VALUES 
                (1, 'Push Up', 'Push-ups are exercises to strengthen your arms and \nchest muscles. They are done by lying with your face \ntowards the floor and pushing with your hands to \nraise your body until your arms are straight.', 10, 1), 
                (2, "Sit Up", "Sit-ups are exercises that you do to strengthen your \nstomach muscles. They involve sitting up from a lying \nposition while keeping your legs straight on the floor.", 20, 2),
                (3, "Pull Up", "A pull-up is an upper-body strength exercise. The \npull-up is a closed-chain movement where the body \nis suspended by the hands and pulls up.", 30, 3)
            """)
        
        if not os.path.exists("final_project.db"):
            self.conn = sqlite3.connect("final_project.db")
            c = self.conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS final_project (
            final_project_id integer PRIMARY KEY ,
            name text,
            course_id integer,
            question text
            )
            """)
        
        if not os.path.exists("final_project_answer.db"):
            self.conn = sqlite3.connect("final_project_answer.db")
            c = self.conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS final_project_answer (
            course_id integer,
            final_project_id integer,
            user_id integer
            answer text
            )
            """)
            
            self.conn.commit()
            self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.start()
    sys.exit(app.exec())