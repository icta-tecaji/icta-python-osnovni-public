import sys
import time

from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class Worker(QRunnable):
    """Worker thread."""

    @pyqtSlot()
    def run(self) -> None:
        """Our long running task."""
        print("Task started")
        time.sleep(5)
        print("Task finished")


class MainWindow(QMainWindow):
    """Main window."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__(parent=None)
        self.setWindowTitle("Hello QT")

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Max thread count: {thread_count}")

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
        worker = Worker()
        self.threadpool.start(worker)

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
