"""Signals and slots example."""

import sys
from functools import partial

from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def greet(name: str):
    """Slot function."""
    if msgLabel.text():
        msgLabel.setText("")
    else:
        msgLabel.setText(f"Hello, {name}!")


app = QApplication([])
window = QWidget()
window.setWindowTitle("PyQt6 Signals and Slots Example")
layout = QVBoxLayout()

btn = QPushButton("Greet")
btn.clicked.connect(partial(greet, "Luka"))

layout.addWidget(btn)
msgLabel = QLabel("")
layout.addWidget(msgLabel)
window.setLayout(layout)

window.show()
sys.exit(app.exec())
