import sys
import time

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """Main window."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__(parent=None)
        self.setWindowTitle("Hello QT")

        self.counter = 0

        layout = QVBoxLayout()
        self.label = QLabel("Start")
        button = QPushButton("DANGER!")
        button.clicked.connect(self._on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def _on_button_click(self):
        for n in range(5):
            QApplication.processEvents()
            time.sleep(1)

    def recurring_timer(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")


def main() -> None:
    """Main function."""
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
