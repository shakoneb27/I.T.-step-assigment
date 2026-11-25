"""
Calculator console application.

Features: +, -, *, / on two numbers, input validation, calculation history
saved to a text file (create / append / delete), OOP with inheritance,
encapsulation and polymorphism.
"""

import math
import os
from abc import ABC, abstractmethod

HISTORY_FILE = "history.txt"


# input helpers 
def read_number(prompt):
    """Read a valid number (int or float) from the user."""
    while True:
        text = input(prompt).strip().replace(",", ".")
        try:
            number = float(text)
        except ValueError:
            print("Invalid number, please try again.")
            continue
        if not math.isfinite(number):          # reject nan / inf
            print("Number is not valid, please try again.")
            continue
        return number


# operations 
    """Abstract base class for an arithmetic operation."""

    def __init__(self, symbol):
        self._symbol = symbol            # encapsulated attribute

    @property
    def symbol(self):
        return self._symbol

    @abstractmethod
    def apply(self, a, b):
        """Return the result of the operation."""


class Addition(Operation):
    def __init__(self):
        super().__init__("+")

    def apply(self, a, b):
        return a + b


class Subtraction(Operation):
    def __init__(self):
        super().__init__("-")

    def apply(self, a, b):
        return a - b


class Multiplication(Operation):
    def __init__(self):
        super().__init__("*")

    def apply(self, a, b):
        return a * b


class Division(Operation):
    def __init__(self):
        super().__init__("/")

    def apply(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b


# calculator 
class Calculator:
    """Chooses an operation by symbol and stores history."""

    def __init__(self):
        # list of operation objects (polymorphism: same apply() interface)
        self._operations = [Addition(), Subtraction(), Multiplication(), Division()]
        self._history = []               # list of strings
        self._last_result = None         # result of the previous calculation

    @property
    def last_result(self):
        return self._last_result

    def find_operation(self, symbol):
        """Return the operation object for a symbol, or None."""
        for operation in self._operations:
            if operation.symbol == symbol:
                return operation
        return None

    def calculate(self, a, b, symbol):
        """Calculate, store the record in history and return the result."""
        operation = self.find_operation(symbol)
        if operation is None:
            raise ValueError("Unknown operation. Use +, -, * or /.")
        result = operation.apply(a, b)
        self._last_result = result
        record = f"{a:g} {symbol} {b:g} = {result:g}"
        self._history.append(record)
        self._append_to_file(record)
        return result
        
    @staticmethod
    def _append_to_file(record):
        """Create the file if needed and append one record."""
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(record + "\n")

    @staticmethod
    def read_history_file():
        """Return all saved history lines."""
        if not os.path.exists(HISTORY_FILE):
            return []
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    @staticmethod
    def remove_last_record():
        """Edit the file: delete the last saved record."""
        lines = Calculator.read_history_file()
        if not lines:
            return False
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            for line in lines[:-1]:
                file.write(line + "\n")
        return True

    @staticmethod
    def delete_history_file():
        """Delete the history file."""
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            return True
        return False


def print_menu():
    print("\n===== CALCULATOR =====")
    print("1. Calculate")
    print("2. Show history")
    print("3. Remove last history record")
    print("4. Delete history file")
    print("0. Exit")


def run_calculation(calculator):
    """Ask for numbers and an operation, then show the result."""
    if calculator.last_result is not None and \
            input(f"Use previous result ({calculator.last_result:g}) as first number? (y/n): ").strip().lower() == "y":
        a = calculator.last_result
    else:
        a = read_number("First number: ")
    b = read_number("Second number: ")
    symbol = input("Operation (+, -, *, /): ").strip()
    try:
        print(f"Result: {calculator.calculate(a, b, symbol):g}")
    except ValueError as error:
        print(f"Error: {error}")


def main():
    """Run the menu until the user chooses Exit (never crashes on Ctrl+C / Ctrl+D)."""
    calculator = Calculator()
    try:
        while True:
            print_menu()
            choice = input("Choice: ").strip()
            if choice == "1":
                run_calculation(calculator)
            elif choice == "2":
                lines = calculator.read_history_file()
                if lines:
                    for number, line in enumerate(lines, start=1):
                        print(f"{number}. {line}")
                else:
                    print("History is empty.")
            elif choice == "3":
                print("Removed." if calculator.remove_last_record() else "Nothing to remove.")
            elif choice == "4":
                print("File deleted." if calculator.delete_history_file() else "No file found.")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    except (KeyboardInterrupt, EOFError):
        print()                                # input interrupted: exit cleanly
    print("Goodbye!")


if __name__ == "__main__":
    main()
