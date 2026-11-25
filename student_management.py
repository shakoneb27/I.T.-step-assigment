"""
Student management system (OOP project).

Classes: Person (base), Student (inherits Person), StudentManager.
Menu: add student, show all, find by roll number, update grade, delete, exit.
Data is stored in a text file; all input is validated.
"""

import os

STUDENTS_FILE = "students.txt"
VALID_GRADES = ["A", "B", "C", "D", "E", "F"]


# models
class Person:
    """Base class with a validated name."""

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value or "|" in value or any(ch.isdigit() for ch in value):
            raise ValueError("Name must not be empty, contain digits or '|'.")
        self._name = value

    def describe(self):
        return f"Name: {self._name}"


class Student(Person):
    """Student with name (str), roll number (int) and grade (char)."""

    def __init__(self, name, roll_number, grade):
        super().__init__(name)
        self.roll_number = roll_number
        self.grade = grade

    @property
    def roll_number(self):
        return self._roll_number

    @roll_number.setter
    def roll_number(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Roll number must be an integer.")
        if value <= 0:
            raise ValueError("Roll number must be positive.")
        self._roll_number = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        value = str(value).strip().upper()
        if value not in VALID_GRADES:
            raise ValueError(f"Grade must be one of: {', '.join(VALID_GRADES)}.")
        self._grade = value

    def describe(self):  # polymorphism: extends Person.describe()
        return f"{super().describe()} | Roll number: {self._roll_number} | Grade: {self._grade}"

    def to_line(self):
        return f"{self._name}|{self._roll_number}|{self._grade}"


# manager 
class StudentManager:
    """Keeps students in a list and in a text file."""

    def __init__(self, path=STUDENTS_FILE):
        self._path = path
        self._students = []         # list of Student objects
        self._load()

    def _load(self):
        if not os.path.exists(self._path):
            return
        with open(self._path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 3:
                    continue
                try:
                    self._students.append(Student(parts[0], parts[1], parts[2]))
                except ValueError:
                    continue

    def _save(self):
        with open(self._path, "w", encoding="utf-8") as file:
            for student in self._students:
                file.write(student.to_line() + "\n")

    def find(self, roll_number):
        """Return the student with this roll number or None."""
        for student in self._students:
            if student.roll_number == roll_number:
                return student
        return None

    def add(self, student):
        if self.find(student.roll_number) is not None:
            raise ValueError("A student with this roll number already exists.")
        self._students.append(student)
        self._save()

    def all(self):
        return list(self._students)

    def update_grade(self, roll_number, grade):
        student = self.find(roll_number)
        if student is None:
            raise ValueError("Student not found.")
        student.grade = grade       # validated by the setter
        self._save()

    def delete(self, roll_number):
        student = self.find(roll_number)
        if student is None:
            return False
        self._students.remove(student)
        self._save()
        return True

def read_roll_number(prompt):
    """Read a positive integer roll number."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            print("Roll number must be positive.")
        except ValueError:
            print("Roll number must be an integer.")


def add_student(manager):
    while True:
        try:
            name = input("Name: ")
            roll = input("Roll number: ")
            grade = input("Grade (A-F): ")
            manager.add(Student(name, roll, grade))
            print("Student added.")
            return
        except ValueError as error:
            print(f"Error: {error} Please try again.")


def main():
    manager = StudentManager()
    while True:
        print("\n===== STUDENT MANAGEMENT =====")
        print("1. Add student\n2. Show all students\n3. Find student by roll number")
        print("4. Update student grade\n5. Delete student\n0. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_student(manager)
        elif choice == "2":
            students = manager.all()
            if not students:
                print("No students yet.")
            for student in students:
                print(student.describe())
        elif choice == "3":
            student = manager.find(read_roll_number("Roll number: "))
            print(student.describe() if student else "Student not found.")
        elif choice == "4":
            roll = read_roll_number("Roll number: ")
            try:
                manager.update_grade(roll, input("New grade (A-F): "))
                print("Grade updated.")
            except ValueError as error:
                print(f"Error: {error}")
        elif choice == "5":
            print("Deleted." if manager.delete(read_roll_number("Roll number: ")) else "Student not found.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()