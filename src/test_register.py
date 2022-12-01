import sys

from PyQt6.QtWidgets import QApplication

from register_window import RegisterWindow

app = QApplication(sys.argv)
window = RegisterWindow()

def test_showPassword():
    window.toggleShowPassword()
    assert window.showPassword == True

def test_emailValidation():
    assert window.emailValidation("wrongEmail@") == False
    assert window.emailValidation("wrongEmail@google.com") == True