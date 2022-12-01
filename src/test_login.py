import sys

from PyQt6.QtWidgets import QApplication

from login_window import LoginWindow

app = QApplication(sys.argv)
window = LoginWindow()

def test_window():
    assert window.showPassword == False

def test_clearForm():
    window.passwordEdit.setText("blablabla")
    window.usernameEdit.setText("blablabla")
    assert window.passwordEdit.text() != '' and window.usernameEdit.text() != ''
    window.clearForm()
    assert window.passwordEdit.text() == '' and window.usernameEdit.text() == ''