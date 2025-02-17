"""Horizontal layout example."""

import sys

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle("PyQt6 Horizontal Layout Example")

layout = QHBoxLayout()
layout.addWidget(QPushButton("Left"))
layout.addWidget(QPushButton("Center"))
layout.addWidget(QPushButton("Right"))
window.setLayout(layout)

window.show()
sys.exit(app.exec())
