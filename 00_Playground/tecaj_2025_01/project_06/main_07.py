"""Main window-style application."""

import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QToolBar


class MainWindow(QMainWindow):
    """Main window."""

    def __init__(self) -> None:
        """Initialize the window."""
        super().__init__(parent=None)
        self.setWindowTitle("PyQt6 Main Window Example")
        self.setCentralWidget(QLabel("I'm the central widget"))
        self._create_menu()
        self._create_tool_bar()
        self._create_status_bar()

    def _create_menu(self) -> None:
        """Create the main menu."""
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _create_tool_bar(self) -> None:
        """Create the toolbar."""
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        status = QStatusBar()
        status.showMessage("I'm the status bar")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
