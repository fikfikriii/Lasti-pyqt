import sqlite3
import sys

from PyQt6.QtWidgets import QApplication

from add_history import addHistory
from add_workout import trainer_AddWorkout

app = QApplication(sys.argv)
window = addHistory()
window2 = trainer_AddWorkout()

def test_addhistory():
    conn = sqlite3.connect("fitpal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM workout_history")
    res = c.fetchall()
    window.addHistory()
    # Seharusnya, tidak ada yang berubah
    c.execute("SELECT * FROM workout_history")
    res2 = c.fetchall()
    return res == res2

def test_addworkout():
    conn = sqlite3.connect("fitpal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM list_olahraga")
    res = c.fetchall()
    window2.addWorkout()
    # Seharusnya, tidak ada yang berubah
    c.execute("SELECT * FROM list_olahraga")
    res2 = c.fetchall()
    return res == res2