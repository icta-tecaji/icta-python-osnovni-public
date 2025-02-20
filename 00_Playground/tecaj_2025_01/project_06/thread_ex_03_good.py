import sys
import time
import traceback
from typing import Callable

from loguru import logger
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget


class WorkerSignals(QObject):
    """Worker signals."""

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(float)


class Worker(QRunnable):
    """Worker thread."""

    def __init__(self, fn: Callable, *args, **kwargs) -> None:
        """Initialize worker thread."""
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self) -> None:
        """Our long running task."""
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as err:  # noqa: BLE001
            logger.error(f"{type(err).__name__} - {err}")
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


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
        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(50, 50, 250, 30)
        button.clicked.connect(self._on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(button)
        layout.addWidget(self.prog_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def long_running_task(self, progress_callback) -> str:
        print("Task started")
        for n in range(10):
            time.sleep(1)
            value = self.prog_bar.value()
            self.prog_bar.setValue(value + 10)
            progress_callback.emit(n * 100 / 9)

        return "Done."

    def reset_progressbar(self):
        self.prog_bar.setValue(0)

    def _on_button_click(self):
        worker = Worker(self.long_running_task)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.reset_progressbar()

    def progress_fn(self, n):
        print(f"{n:.1f}% done")


def main() -> None:
    """Main function."""
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
