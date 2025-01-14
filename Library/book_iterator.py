from abc import ABC, abstractmethod
from typing import List, Dict, Any, Iterator
from collections import defaultdict


class BookIterator(ABC):
    """Abstract base class for book iterators"""

    @abstractmethod
    def __iter__(self) -> Iterator:
        pass

    @abstractmethod
    def __next__(self) -> 'Book':
        pass


class ChronologicalIterator(BookIterator):
    """Iterates through books in chronological order"""

    def __init__(self, books: List['Book'], reverse: bool = False):
        self._books = sorted(books, key=lambda x: x.year, reverse=reverse)
        self._index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> 'Book':
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book


class AlphabeticalIterator(BookIterator):
    """Iterates through books in alphabetical order"""

    def __init__(self, books: List['Book'], by_author: bool = False):
        self._books = sorted(books, key=lambda x: x.author if by_author else x.title)
        self._index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> 'Book':
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book


class GenreIterator(BookIterator):
    """Iterates through books grouped by genre"""

    def __init__(self, books: List['Book']):
        # Group books by genre
        self._genre_books: Dict[str, List['Book']] = defaultdict(list)
        for book in books:
            self._genre_books[book.genre].append(book)

        # Sort genres and books within each genre
        self._genres = sorted(self._genre_books.keys())
        for genre in self._genres:
            self._genre_books[genre].sort(key=lambda x: x.title)

        self._genre_index = 0
        self._book_index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> 'Book':
        if self._genre_index >= len(self._genres):
            raise StopIteration

        current_genre = self._genres[self._genre_index]
        current_genre_books = self._genre_books[current_genre]

        if self._book_index >= len(current_genre_books):
            self._genre_index += 1
            self._book_index = 0
            return self.__next__()

        book = current_genre_books[self._book_index]
        self._book_index += 1
        return book

    def current_genre(self) -> str:
        """Get the current genre being iterated"""
        if self._genre_index >= len(self._genres):
            return None
        return self._genres[self._genre_index]


class PopularityIterator(BookIterator):
    """Iterates through books based on their popularity (waiting list size)"""

    def __init__(self, books: List['Book'], library_system: 'LibrarySystem'):
        self._books = sorted(
            books,
            key=lambda x: len(library_system.get_waiting_list(x.title)),
            reverse=True
        )
        self._index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> 'Book':
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book


class AvailabilityIterator(BookIterator):
    """Iterates through books based on their availability"""

    def __init__(self, books: List['Book'], available_only: bool = True):
        self._books = sorted(
            [b for b in books if b.is_available == available_only],
            key=lambda x: x.title
        )
        self._index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> 'Book':
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book


# Add this method to LibrarySystem class:
def get_iterator(self, iterator_type: str, **kwargs) -> BookIterator:
    """
    Get a specific type of book iterator

    Args:
        iterator_type: Type of iterator ('chronological', 'alphabetical', 'genre', 'popularity', 'availability')
        **kwargs: Additional arguments for specific iterators

    Returns:
        BookIterator: The requested iterator
    """
    books = list(self.books.values())

    if iterator_type == 'chronological':
        return ChronologicalIterator(books, reverse=kwargs.get('reverse', False))
    elif iterator_type == 'alphabetical':
        return AlphabeticalIterator(books, by_author=kwargs.get('by_author', False))
    elif iterator_type == 'genre':
        return GenreIterator(books)
    elif iterator_type == 'popularity':
        return PopularityIterator(books, self)
    elif iterator_type == 'availability':
        return AvailabilityIterator(books, available_only=kwargs.get('available_only', True))
    else:
        raise ValueError(f"Unknown iterator type: {iterator_type}")


# Example usage:
"""
# Get chronological iterator (newest first)
chronological_iter = library.get_iterator('chronological', reverse=True)
print("Newest books:")
for book in chronological_iter:
    print(f"{book.title} ({book.year})")

# Get genre iterator
genre_iter = library.get_iterator('genre')
current_genre = None
for book in genre_iter:
    if isinstance(genre_iter, GenreIterator):
        new_genre = genre_iter.current_genre()
        if new_genre != current_genre:
            current_genre = new_genre
            print(f"\n{current_genre}:")
    print(f"- {book.title}")
"""