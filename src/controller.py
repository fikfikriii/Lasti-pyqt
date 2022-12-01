import os.path
import sqlite3
import sys
from tkinter import E

from PyQt6.QtWidgets import QApplication

from register_window import RegisterWindow
from login_window import LoginWindow
from user_course import UserCourse
from display_course_student import DisplayCourseStudent
from instructor_course import InstructorCourse
from instructor_dashboard import InstructorDashboard

class Controller:
    def __init__(self):
        self.initializeDatabase()
        self.loginWindow = LoginWindow()
        self.loginWindow.switch.connect(self.fromLogin)
        self.registerWindow = RegisterWindow()
        self.registerWindow.switch.connect(self.fromRegister)
        self.userCourse = UserCourse()
        self.userCourse.switch.connect(self.fromUserCourse)
        self.displayCourseStudent = DisplayCourseStudent()
        self.displayCourseStudent.switch.connect(self.fromDisplayCourseStudent)
        self.instructorCourse = InstructorCourse()
        self.instructorCourse.switch.connect(self.fromInstructorCourse)
        self.instructorDashboard = InstructorDashboard()
        self.instructorDashboard.switch.connect(self.fromInstructorDashboard)
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
        elif page == "user_course":
            self.userCourse.updateUser(user)
            self.userCourse.show()
        elif page == "instructor_course":
            self.instructorCourse.updateUser(user)
            self.instructorCourse.show()        

    def fromUserCourse(self, page, user, course):
        self.userCourse.close()
        if page == "login":
            self.loginWindow.clearForm()
            self.loginWindow.show()
        elif page == "display_course_student":
            self.displayCourseStudent.updateUser(user)
            self.displayCourseStudent.updateCourse(course)
            self.displayCourseStudent.fetchFinalProject()
            self.displayCourseStudent.show()
            
    def fromDisplayCourseStudent(self, page, user):
        self.displayCourseStudent.close()
        if page == 'user_course':
            self.userCourse.updateUser(user)
            self.userCourse.show()
            
    def fromInstructorCourse(self, page, instructor, course):
        self.instructorCourse.close()
        if page == "login":
            self.loginWindow.clearForm()
            self.loginWindow.show()
        elif page == "instructor_dashboard":
            self.instructorDashboard.updateUser(instructor)
            self.instructorDashboard.updateCourse(course)
            self.instructorDashboard.fetchAnswer()
            self.instructorDashboard.show()

    def fromInstructorDashboard(self, page, instructor):
        self.instructorDashboard.close()
        if page == 'instructor_course':
            self.instructorCourse.updateUser(instructor)
            self.instructorCourse.show()

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