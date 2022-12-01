import re
import sqlite3
import sys

import bcrypt
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QRadioButton, QWidget)

from custom_widgets import ClickableLabel

card_bg = '#3E405B'
gray = 'rgba(255, 255, 255, 0.8)'


class RegisterWindow(QWidget):
    switch = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setUpRegisterWindow()
        self.conn = sqlite3.connect("fitpal.db")

    def setUpRegisterWindow(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("FitPal - Register")
        self.setUpWidgets()

    def setUpWidgets(self):
        # Set warna background
        self.setStyleSheet('background-color: #28293D')

        # Set up font
        inter14 = QFont()
        inter14.setFamily("Inter")
        inter14.setPixelSize(14)

        inter16 = QFont()
        inter16.setFamily("Inter")
        inter16.setPixelSize(16)

        inter24 = QFont()
        inter24.setFamily("Inter")
        inter24.setPixelSize(24)

        # Card label
        card = QLabel(self)
        cardImg = QPixmap("../img/register-card.png")
        card.setPixmap(cardImg)
        card.move(309, 63)

        # Heading label
        heading = QLabel(self)
        heading.setText("Welcome to FitPal!")
        heading.setFont(inter24)
        heading.setStyleSheet(f'color: {gray}; background-color: {card_bg}')
        heading.move(533, 105)

        # Subheading label
        subheading = QLabel(self)
        subheading.setText(
            "Create an account to enjoy a new experience in working out!")
        subheading.setFont(inter16)
        subheading.setStyleSheet(f'color: {gray}; background-color: {card_bg}')
        subheading.move(404, 146)

        # Full name input
        self.nameEdit = QLineEdit(self)
        self.nameEdit.setPlaceholderText("Full name")
        self.nameEdit.setFixedSize(466, 46)
        self.nameEdit.setFont(inter16)
        self.nameEdit.setStyleSheet('''
        padding: 11px 30px 11px 30px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        background-color: #3E405B
        ''')
        self.nameEdit.move(407, 194)

        # Username input
        self.unameEdit = QLineEdit(self)
        self.unameEdit.setPlaceholderText("Username")
        self.unameEdit.setFixedSize(466, 46)
        self.unameEdit.setFont(inter16)
        self.unameEdit.setStyleSheet('''
        padding: 11px 30px 11px 30px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        background-color: #3E405B
        ''')
        self.unameEdit.move(407, 255)

        # Email input
        self.emailEdit = QLineEdit(self)
        self.emailEdit.setPlaceholderText("Email")
        self.emailEdit.setFixedSize(466, 46)
        self.emailEdit.setFont(inter16)
        self.emailEdit.setStyleSheet('''
        padding: 11px 30px 11px 30px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        background-color: #3E405B
        ''')
        self.emailEdit.move(407, 316)

        # Password input
        self.passwordEdit = QLineEdit(self)
        self.passwordEdit.setPlaceholderText("Password")
        self.passwordEdit.setFixedSize(466, 46)
        self.passwordEdit.setFont(inter16)
        self.passwordEdit.setStyleSheet('''
        padding: 11px 30px 11px 30px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        background-color: #3E405B
        ''')
        self.passwordEdit.move(407, 377)
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # Register type label
        typeLabel = QLabel(self)
        typeLabel.setFont(inter14)
        typeLabel.setText("I want to register as a:")
        typeLabel.setStyleSheet(f'color: {gray}; background-color: {card_bg}')
        typeLabel.move(565, 438)

        # User radio button
        self.rbUser = QRadioButton(self)
        self.rbUser.move(565, 465)
        self.rbUser.setStyleSheet(
            f'background-color: {card_bg}; color: {gray}')
        self.rbUser.setText("User")
        self.rbUser.setFont(inter14)
        self.rbUser.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Trainer radio button
        self.rbTrainer = QRadioButton(self)
        self.rbTrainer.move(565, 487)
        self.rbTrainer.setStyleSheet(
            f'background-color: {card_bg}; color: {gray}')
        self.rbTrainer.setText("Trainer")
        self.rbTrainer.setFont(inter14)
        self.rbTrainer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Register push button
        self.registerButton = QPushButton(self)
        self.registerButton.setText("Register")
        self.registerButton.setFixedSize(183, 48)
        self.registerButton.move(548, 523)
        self.registerButton.setStyleSheet('''
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
        self.registerButton.setFont(inter16)
        self.registerButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.registerButton.clicked.connect(self.register)

        # Already have an account? label
        label = QLabel(self)
        label.setText("Already have an account?")
        label.setFont(inter14)
        label.setStyleSheet(
            'color: rgba(255, 255, 255, 0.8); background-color: #3E405B')
        label.move(553, 588)

        # Register here label
        logIn = ClickableLabel(self)
        logIn.setText("Log in")
        logIn.setFont(inter16)
        logIn.setStyleSheet('''
        QLabel {
            color: #3EEBBE; 
            text-decoration: underline; 
            background-color: #3E405B
        }
        QLabel:hover {
            color: #68FCD6;
        }
        '''
                            )
        logIn.move(616, 609)
        logIn.clicked.connect(self.showLoginWindow)
        logIn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Eye icon
        eyeIcon = ClickableLabel(self)
        eyeIconImg = QPixmap("../img/eye-icon.png")
        eyeIcon.setPixmap(eyeIconImg)
        eyeIcon.move(819, 388)
        eyeIcon.setStyleSheet("background-color: #3E405B")
        eyeIcon.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Eye icon click handling
        self.showPassword = False
        eyeIcon.clicked.connect(self.toggleShowPassword)

    def showLoginWindow(self):
        self.switch.emit()

    def toggleShowPassword(self):
        self.showPassword = not (self.showPassword)
        if (self.showPassword):
            self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def emailValidation(self, email):
        validEmail = r"[A-Za-z0-9._]+@[A-Za-z0-9.]+\.[A-Z|a-z]{2,}"
        if re.match(validEmail, email):
            return True
        else:
            return False
    
    def hashPassword(self, password):
        bytePass = password.encode('utf-8')
        return bcrypt.hashpw(bytePass, bcrypt.gensalt())

    def register(self):
        if (self.nameEdit.text() == '' or self.unameEdit.text() == '' or self.emailEdit.text() == '' or self.passwordEdit.text() == '' or (not self.rbUser.isChecked() and not self.rbTrainer.isChecked())):
            msgBox = QMessageBox()
            msgBox.setText("<p>Please fill out the form properly!</p>")
            msgBox.setWindowTitle("Registration Failed")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStyleSheet("background-color: white")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        if not self.emailValidation(self.emailEdit.text()):
            msgBox = QMessageBox()
            msgBox.setText("<p>Please input correct email!</p>")
            msgBox.setWindowTitle("Registration Failed")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStyleSheet("background-color: white")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        if len(self.passwordEdit.text()) < 8:
            msgBox = QMessageBox()
            msgBox.setText("<p>Password is too short!</p>")
            msgBox.setWindowTitle("Registration Failed")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStyleSheet("background-color: white")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        c = self.conn.cursor()
        c.execute(
            f"SELECT * FROM user WHERE username = '{self.unameEdit.text()}'")
        if (c.fetchone() != None):
            msgBox = QMessageBox()
            msgBox.setText("<p>Username already registered!</p>")
            msgBox.setWindowTitle("Registration Failed")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStyleSheet("background-color: white")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        c.execute(
            f"SELECT * FROM user WHERE email = '{self.emailEdit.text()}'")
        if (c.fetchone() != None):
            msgBox = QMessageBox()
            msgBox.setText("<p>Email already registered!</p>")
            msgBox.setWindowTitle("Registration Failed")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStyleSheet("background-color: white")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        hashedPass = self.hashPassword(self.passwordEdit.text())
        hashedPass = hashedPass.decode()
        if (self.rbUser.isChecked()):
            c.execute(
                f"INSERT INTO user (fullname, username, email, password, type) VALUES ('{self.nameEdit.text()}', '{self.unameEdit.text()}', '{self.emailEdit.text()}', '{hashedPass}', 'user')")
            self.conn.commit()
        else:
            c.execute(
                f"INSERT INTO user (fullname, username, email, password, type) VALUES ('{self.nameEdit.text()}', '{self.unameEdit.text()}', '{self.emailEdit.text()}', '{hashedPass}', 'trainer')")
            self.conn.commit()
        # Tunjukkan registrasi berhasil
        msgBox = QMessageBox()
        msgBox.setText(f"""<p>Welcome to FitPal, {self.nameEdit.text()}!</p>
    <p>You will now be prompted to log in.</p>""")
        msgBox.setWindowTitle("Registration Successful")
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setStyleSheet("background-color: white")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
        # Clear form inputs
        self.nameEdit.clear()
        self.unameEdit.clear()
        self.emailEdit.clear()
        self.passwordEdit.clear()
        # Emit signal to controller
        self.switch.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    sys.exit(app.exec())
