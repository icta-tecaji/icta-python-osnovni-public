"""PyCalc is a simple calculator built with Python and PyQt."""

import sys
from functools import partial
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40


def evaluate_expression(expression: str) -> str:
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))  # noqa: S307
    except Exception:  # noqa: BLE001
        result = ERROR_MSG
    return result


class PyCalcMainWindow(QMainWindow):
    """PyCalc's main window (GUI)."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__(parent=None)
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        # general layout
        self.generalLayout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(self.generalLayout)
        self.setCentralWidget(central_widget)
        # create display and buttons
        self._create_display()
        self._create_buttons()

    def _create_display(self) -> None:
        """Create the display."""
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _create_buttons(self) -> None:
        """Create the buttons."""
        self.button_map = {}
        button_layout = QGridLayout()
        keyboard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.button_map[key] = QPushButton(key)
                self.button_map[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                button_layout.addWidget(self.button_map[key], row, col)
        self.generalLayout.addLayout(button_layout)

    def set_display_text(self, text: str) -> None:
        """Set the display text."""
        self.display.setText(text)
        self.display.setFocus()

    def display_text(self) -> str:
        """Get the display text."""
        return self.display.text()

    def clear_display(self) -> None:
        """Clear the display."""
        self.set_display_text("")


class PyCalcCtrl:
    """PyCalc Controller class."""

    def __init__(self, model: Callable, view: PyCalcMainWindow) -> None:
        """Initialize the controller."""
        self._evaluate = model
        self._view = view
        self._connect_signals_and_slots()

    def _calculate_result(self) -> None:
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.display_text())
        self._view.set_display_text(result)

    def _build_expression(self, sub_exp: str) -> None:
        """Build expression."""
        if self._view.display_text() == ERROR_MSG:
            self._view.clear_display()
        expression = self._view.display_text() + sub_exp
        self._view.set_display_text(expression)

    def _connect_signals_and_slots(self) -> None:
        """Connect signals and slots."""
        for key_symbol, button in self._view.button_map.items():
            if key_symbol not in {"=", "C"}:
                button.clicked.connect(partial(self._build_expression, key_symbol))

        self._view.button_map["="].clicked.connect(self._calculate_result)
        self._view.display.returnPressed.connect(self._calculate_result)
        self._view.button_map["C"].clicked.connect(self._view.clear_display)


def main() -> None:
    """Run Main function for PyCalc."""
    pycalc_app = QApplication([])
    pycalc_window = PyCalcMainWindow()
    pycalc_window.show()
    PyCalcCtrl(model=evaluate_expression, view=pycalc_window)
    sys.exit(pycalc_app.exec())


if __name__ == "__main__":
    main()
