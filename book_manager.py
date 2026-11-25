"""
Book management console application (OOP project).

Classes: Book, EBook (inherits Book), BookManager.
Features: add a book, list all books, search by title, delete a book,
data stored in a text file, input validation and a demo example.
"""

import os
from datetime import date

BOOKS_FILE = "books.txt"


# ------------------------------- models -----------------------------------
class Book:
    """A book with title, author and publication year."""

    def __init__(self, title, author, year):
        # setters below validate the values (encapsulation)
        self.title = title
        self.author = author
        self.year = year

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        value = str(value).strip()
        if not value or "|" in value:
            raise ValueError("Title must not be empty or contain '|'.")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        value = str(value).strip()
        if not value or "|" in value:
            raise ValueError("Author must not be empty or contain '|'.")
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Year must be an integer.")
        if value < 1000 or value > date.today().year:
            raise ValueError(f"Year must be between 1000 and {date.today().year}.")
        self._year = value

    def describe(self):
        """Return a readable description (overridden in subclasses)."""
        return f"'{self._title}' by {self._author} ({self._year})"

    def to_line(self):
        """Serialize for the text file."""
        return f"book|{self._title}|{self._author}|{self._year}|"


class EBook(Book):
    """Electronic book: a Book with a file size in MB (inheritance)."""

    def __init__(self, title, author, year, size_mb):
        super().__init__(title, author, year)
        try:
            size_mb = float(size_mb)
        except (TypeError, ValueError):
            raise ValueError("Size must be a number.")
        if size_mb <= 0:
            raise ValueError("Size must be positive.")
        self._size_mb = size_mb

    def describe(self):  # polymorphism: same method, different output
        return f"{super().describe()} [E-book, {self._size_mb:g} MB]"

    def to_line(self):
        return f"ebook|{self._title}|{self._author}|{self._year}|{self._size_mb:g}"


# ------------------------------- manager ----------------------------------
class BookManager:
    """Manages a list of books and stores them in a file."""

    def __init__(self, path=BOOKS_FILE):
        self._path = path
        self._books = []            # list of Book / EBook objects
        self._load()

    def _load(self):
        """Read books from the file (if it exists)."""
        if not os.path.exists(self._path):
            return
        with open(self._path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 5:
                    continue
                try:
                    if parts[0] == "ebook":
                        self._books.append(EBook(parts[1], parts[2], parts[3], parts[4]))
                    else:
                        self._books.append(Book(parts[1], parts[2], parts[3]))
                except ValueError:
                    continue        # skip broken lines

    def _save(self):
        """Rewrite the whole file from the list."""
        with open(self._path, "w", encoding="utf-8") as file:
            for book in self._books:
                file.write(book.to_line() + "\n")

    def add_book(self, book):
        """Add a book to the list and save."""
        self._books.append(book)
        self._save()

    def list_books(self):
        """Return a copy of the list of books."""
        return list(self._books)

    def search_by_title(self, text):
        """Return books whose title contains the text (case-insensitive)."""
        text = text.strip().lower()
        return [b for b in self._books if text in b.title.lower()]

    def delete_book(self, title):
        """Delete books with exactly this title; return how many were removed."""
        before = len(self._books)
        self._books = [b for b in self._books if b.title.lower() != title.strip().lower()]
        self._save()
        return before - len(self._books)


# --------------------------------- UI -------------------------------------
def ask_book():
    """Ask the user for book data until it is valid; return a Book/EBook."""
    while True:
        try:
            title = input("Title: ")
            author = input("Author: ")
            year = input("Publication year: ")
            if input("Is it an e-book? (y/n): ").strip().lower() == "y":
                return EBook(title, author, year, input("Size in MB: "))
            return Book(title, author, year)
        except ValueError as error:
            print(f"Error: {error} Please try again.")


def print_books(books):
    if not books:
        print("No books found.")
    for number, book in enumerate(books, start=1):
        print(f"{number}. {book.describe()}")


def demo():
    """Demonstration example: add, list and search (uses a separate file)."""
    print("\n--- DEMO ---")
    manager = BookManager("demo_books.txt")
    manager.add_book(Book("Clean Code", "Robert Martin", 2008))
    manager.add_book(EBook("Python Basics", "John Smith", 2020, 4.5))
    manager.add_book(Book("The Pragmatic Programmer", "Andrew Hunt", 1999))
    print("All books:")
    print_books(manager.list_books())
    print("Search 'python':")
    print_books(manager.search_by_title("python"))
    os.remove("demo_books.txt")      # clean up the demo file


def main():
    manager = BookManager()
    while True:
        print("\n===== BOOK MANAGER =====")
        print("1. Add book\n2. Show all books\n3. Search by title")
        print("4. Delete book\n5. Run demo\n0. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            manager.add_book(ask_book())
            print("Book added.")
        elif choice == "2":
            print_books(manager.list_books())
        elif choice == "3":
            print_books(manager.search_by_title(input("Title to search: ")))
        elif choice == "4":
            removed = manager.delete_book(input("Exact title to delete: "))
            print(f"Deleted {removed} book(s).")
        elif choice == "5":
            demo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()