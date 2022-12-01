import sys

from PyQt6.QtWidgets import QApplication

from workout_history import WorkoutHistory

app = QApplication(sys.argv)
window = WorkoutHistory()

def test_label():
    assert window.helloLabel.text() == "Hello, John Doe!"

def test_history():
    window.fetchWorkoutHistory()
    assert window.history == []