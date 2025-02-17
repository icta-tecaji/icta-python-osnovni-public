"""Simple first example of a Python program."""

import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle("PyQt6 App Example")
window.setGeometry(100, 100, 280, 80)
hello_msg = QLabel("<h1>Hello, World!</h1>", parent=window)
hello_msg.move(60, 15)

window.show()

sys.exit(app.exec())
