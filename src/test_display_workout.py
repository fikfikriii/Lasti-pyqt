import sys

from PyQt6.QtWidgets import QApplication

from display_workout import DisplayWorkout
from display_workout_trainer import DisplayWorkoutTrainer

app = QApplication(sys.argv)
window = DisplayWorkout()
window2 = DisplayWorkoutTrainer()

def test_fetch():
    window.fetchWorkout()
    window2.fetchWorkout()
    assert len(window.workout) > 0 and len(window2.workout) > 0