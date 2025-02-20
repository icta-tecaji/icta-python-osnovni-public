import sys
import threading
import time
import traceback
import uuid
from functools import partial
from typing import Callable

from loguru import logger
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget


class WorkerSignals(QObject):
    """Worker signals."""

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress_updated = pyqtSignal(int)


class Worker(QRunnable):
    """Worker thread."""

    def __init__(self, fn: Callable, stop_event: threading.Event, *args, **kwargs) -> None:
        """Initialize worker thread."""
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.stop_event = stop_event
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress_updated
        self.kwargs["stop_event"] = self.stop_event

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
        self.counter = 0
        self.setWindowTitle("Hello QT")

        # Store active components
        self.threads = []
        self.progress_bars = []
        self.cancel_buttons = []
        self.labels = []

        # Set up main widget and layout
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Add button to start new workers
        self.start_button = QPushButton("Start New Task")
        self.start_button.clicked.connect(self.start_new_worker)
        layout.addWidget(self.start_button)

        # Container for progress bar
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)
        layout.addWidget(self.progress_container)

        # Set up thread pool
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Max thread count: {thread_count}")

    def start_new_worker(self) -> None:
        """Create a new worker thread and associated progress bar."""
        current_stop_event = threading.Event()

        progress_bar = QProgressBar(self)
        task_label = QLabel(f"Task {uuid.uuid4()}")
        cancel_button = QPushButton("Cancel Task")
        cancel_button.clicked.connect(partial(self.cancel_worker, current_stop_event))
        self.progress_layout.addWidget(progress_bar)
        self.progress_layout.addWidget(task_label)
        self.progress_layout.addWidget(cancel_button)
        self.progress_bars.append(progress_bar)
        self.labels.append(task_label)
        self.cancel_buttons.append(cancel_button)

        worker = Worker(self.long_running_task, current_stop_event)
        # Connect signals
        worker.signals.progress_updated.connect(progress_bar.setValue)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.finished.connect(lambda: self.cleanup_worker(progress_bar, task_label, cancel_button))
        self.threadpool.start(worker)

    def cancel_worker(self, current_stop_event) -> None:
        """Cancel worker thread."""
        if current_stop_event is not None:
            print("Canceling worker")
            current_stop_event.set()

    def cleanup_worker(self, progress_bar, task_label, cancel_button) -> None:
        """Remove worker from list of active workers."""
        # Remove UI components
        self.progress_layout.removeWidget(progress_bar)
        progress_bar.deleteLater()

        self.progress_layout.removeWidget(task_label)
        task_label.deleteLater()

        self.progress_layout.removeWidget(cancel_button)
        cancel_button.deleteLater()

        # Remove worker from list
        self.progress_bars.remove(progress_bar)
        self.labels.remove(task_label)
        self.cancel_buttons.remove(cancel_button)

    def long_running_task(self, progress_callback, stop_event: threading.Event) -> str:
        print("Task started")
        for progress in range(101):
            if stop_event.is_set():
                print("Canceling task")
                progress_callback.emit(0)
                return "Canceled."
            time.sleep(0.1)
            progress_callback.emit(progress)
        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")


def main() -> None:
    """Main function."""
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
