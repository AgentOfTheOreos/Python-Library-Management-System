import csv
from typing import List, Optional
from .book import Book


class BookFactory:
    """
    Factory class for creating and managing Book instances.

    Provides methods to create books, load them from a CSV file,
    and save them to a CSV file.
    """
    @staticmethod
    def create_book(
            title: str,
            author: str,
            copies: int,
            genre: str,
            year: int,
            loaned_copies: int = 0
    ) -> Book:
        """
        Create a single Book instance with the given parameters.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            copies (int): Total number of copies.
            genre (str): The book's genre.
            year (int): Publication year of the book.
            loaned_copies (int): Number of copies currently loaned out (default is 0).

        Returns:
            Book: A new Book instance initialized with the provided data.
        """
        return Book(
            title=title,
            author=author,
            copies=copies,
            genre=genre,
            year=year,
            loaned_copies=loaned_copies
        )

    @staticmethod
    def create_from_csv(filepath: str) -> List[Book]:
        """
        Create multiple Book instances by reading from a CSV file.

        Args:
            filepath (str): Path to the CSV file containing book data.

        Returns:
            List[Book]: A list of Book instances created from the CSV data.

        Raises:
            FileNotFoundError: If the CSV file cannot be found.
            ValueError: If the CSV data is invalid or contains errors.
        """
        books = []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        book = Book.from_dict(row)
                        books.append(book)
                    except (ValueError, KeyError) as e:
                        # Log the error but continue processing other books
                        print(f"Error creating book from row {row}: {str(e)}")
                        continue

        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file at {filepath}")
        except csv.Error as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

        return books

    @staticmethod
    def save_to_csv(books: List[Book], filepath: str) -> None:
        """
        Save a list of Book instances to a CSV file.

        Args:
            books (List[Book]): List of Book instances to save.
            filepath (str): Path where the CSV file should be saved.

        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                if not books:
                    writer = csv.writer(file)
                    writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year'])
                    return

                writer = csv.DictWriter(file, fieldnames=books[0].to_dict().keys())
                writer.writeheader()
                for book in books:
                    writer.writerow(book.to_dict())

        except IOError as e:
            raise IOError(f"Error writing to CSV file: {str(e)}")
