import sys

from PyQt6.QtWidgets import QApplication

from dashboard_trainer import TrainerDashboard
from dashboard_user import UserDashboard

app = QApplication(sys.argv)
windowUser = UserDashboard()
windowTrainer = TrainerDashboard()

def test_labels():
    assert windowUser.helloLabel.text() == "Hello, John Doe!"
    assert windowTrainer.helloLabel.text() == "Hello, John Doe!"