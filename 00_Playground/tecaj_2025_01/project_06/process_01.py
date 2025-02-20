import re
import sys

from loguru import logger
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QProgressBar, QPushButton, QVBoxLayout, QWidget

progress_re = re.compile(r"Total complete: (\d+)%")


def simple_percentage_parser(message: str) -> int:
    """Parse the percentage from a message."""
    match = progress_re.search(message)
    if match is None:
        return 0
    return int(match.group(1))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """MainWindow constructor."""
        super().__init__()

        self.process = None
        main_widget = QWidget()
        layout = QVBoxLayout()

        self.button = QPushButton("Run Script")
        self.button.clicked.connect(self.run_script)
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        layout.addWidget(self.button)
        layout.addWidget(self.progress)
        layout.addWidget(self.text_edit)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def message(self, message_string: str) -> None:
        """Print messages to the text edit."""
        self.text_edit.appendPlainText(message_string)

    def process_finished(self) -> None:
        """Handle the process finishing."""
        if self.process is not None:
            self.message("Script finished.")
            self.message("Exit code: " + str(self.process.exitCode()))
            self.process = None

    def run_script(self) -> None:
        """Run the script."""
        if self.process is None:
            self.message("Running script...")
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.process_finished)
            self.process.start("python", ["project_06/dummy_script.py", "--run-fast", "--total-runs=3"])
        else:
            self.message("Script already running.")
            logger.warning("Script already running.")

    def handle_stderr(self) -> None:
        """Handle standard error output."""
        if self.process is None:
            return
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf-8")
        progress = simple_percentage_parser(stderr)
        if progress:
            self.progress.setValue(progress)
        self.message(stderr)

    def handle_stdout(self) -> None:
        """Handle standard output."""
        if self.process is None:
            return
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf-8")
        self.message(stdout)

    def handle_state(self, state) -> None:
        """Handle the state of the process."""
        states = {
            QProcess.ProcessState.NotRunning: "Not running",
            QProcess.ProcessState.Starting: "Starting",
            QProcess.ProcessState.Running: "Running",
        }
        state_name = states[state]
        self.message("State changed: " + state_name)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
