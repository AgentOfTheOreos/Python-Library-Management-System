from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


class BookInterface(ABC):
    """
    Abstract interface for all books and decorators.
    Defines the common properties and methods that any book-related class must implement.
    """

    @property
    @abstractmethod
    def title(self) -> str:
        """Get the title of the book."""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """Get the author of the book."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the full description of the book, including all features."""
        pass

    @property
    @abstractmethod
    def special_features(self) -> List[str]:
        """Get a list of special features for the book."""
        pass


class Book(BookInterface):
    """
    Represents a book in the library management system.
    Implements the BookInterface for compatibility with decorators.
    """
    title: str
    author: str
    copies: int
    genre: str
    year: int
    loaned_copies: int = 0
    total_borrows: int = 0

    """
    Represents a book in the library management system.
    Implements the BookInterface for compatibility with decorators.
    """
    def __init__(self, title: str, author: str, genre: str, year: int, copies: int, loaned_copies: int = 0, total_borrows: int = 0):
        # Validate input arguments
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        if not author or not isinstance(author, str):
            raise ValueError("Author must be a non-empty string")
        if not isinstance(copies, int) or copies < 0:
            raise ValueError("Number of copies must be a non-negative integer")
        if not genre or not isinstance(genre, str):
            raise ValueError("Genre must be a non-empty string")
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        if not isinstance(loaned_copies, int) or loaned_copies < 0:
            raise ValueError("Number of loaned copies must be a non-negative integer")
        if loaned_copies > copies:
            raise ValueError("Number of loaned copies cannot exceed total copies")
        if not isinstance(total_borrows, int) or total_borrows < 0:
            raise ValueError("Total borrows must be a non-negative integer")

        # Assign validated fields
        self._title = title
        self._author = author
        self.genre = genre
        self.year = year
        self.copies = copies
        self.loaned_copies = loaned_copies
        self.total_borrows = total_borrows

    @property
    def title(self) -> str:
        """
        Get the title of the book.
        """
        return self._title

    @property
    def author(self) -> str:
        """
        Get the author of the book.
        """
        return self._author

    @property
    def available_copies(self) -> int:
        """
        Get the number of copies available for loan.

        Returns:
            int: The number of copies that are not currently loaned out.
        """
        return self.copies - self.loaned_copies

    @property
    def is_available(self) -> bool:
        """
        Check if the book has any copies available for loan.

        Returns:
            bool: True if at least one copy is available, False otherwise.
        """
        return self.available_copies > 0

    @property
    def is_fully_loaned(self) -> bool:
        """
        Check if all copies of the book are currently loaned out.

        Returns:
            bool: True if all copies are loaned out, False otherwise.
        """
        return self.loaned_copies == self.copies

    @property
    def description(self) -> str:
        """
        Get the full description of the book.

        Returns:
            str: A detailed description of the book.
        """
        return f"{self.title} by {self.author} ({self.year})\nGenre: {self.genre}"

    @property
    def special_features(self) -> List[str]:
        """
        Get a list of special features for the book.

        Returns:
            List[str]: An empty list since the base Book class has no special features.
        """
        return []

    def loan(self) -> bool:
        """
        Attempt to loan the book.

        Returns:
            bool: True if the loan was successful (a copy was available),
                  False if no copies were available.
        """
        if self.is_available:
            self.loaned_copies += 1
            self.total_borrows += 1
            return True
        return False

    def return_book(self) -> bool:
        """
        Return a loaned copy of the book.

        Returns:
            bool: True if the return was successful (a copy was loaned out),
                  False if no loaned copies existed to return.
        """
        if self.loaned_copies > 0:
            self.loaned_copies -= 1
            return True
        return False

    def update_copies(self, new_count: int) -> None:
        """
        Update the total number of copies available for the book.

        Args:
            new_count (int): The new total number of copies.

        Raises:
            ValueError: If new_count is negative or if it is less than the
                        current number of loaned copies.
        """
        if new_count < 0:
            raise ValueError("Number of copies cannot be negative")
        if new_count < self.loaned_copies:
            raise ValueError("Cannot reduce total copies below number of loaned copies")
        self.copies = new_count

    def to_dict(self) -> dict:
        """
        Convert the book instance to a dictionary for saving to CSV or other formats.

        Returns:
            dict: A dictionary representation of the book with keys:
                  'title', 'author', 'is_loaned', 'copies', 'genre', 'year'.
        """
        return {
            'title': self.title,
            'author': self.author,
            'is_loaned': 'Yes' if self.is_fully_loaned else 'No',
            'copies': self.copies,
            'genre': self.genre,
            'year': self.year
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        Create a Book instance from a dictionary.

        Args:
            data (dict): A dictionary containing book data with keys:
                         'title', 'author', 'copies', 'genre', 'year', and
                         'is_loaned'.

        Returns:
            Book: An instance of the Book class populated with the given data.
        """
        copies = int(data['copies'])
        # If the book is marked as loaned in the CSV, we assume all copies are loaned
        loaned_copies = copies if data['is_loaned'].lower() == 'yes' else 0

        return cls(
            title=data['title'],
            author=data['author'],
            copies=copies,
            genre=data['genre'],
            year=int(data['year']),
            loaned_copies=loaned_copies
        )
