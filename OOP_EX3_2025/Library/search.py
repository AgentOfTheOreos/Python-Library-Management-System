from abc import ABC, abstractmethod
from typing import List
from .book import Book


class SearchStrategy(ABC):
    """Abstract base class for search strategies"""

    @abstractmethod
    def search(self, books: List[Book], query: str) -> List[Book]:
        """
        Search for books using the strategy's criteria

        Args:
            books: List of books to search through
            query: Search query string

        Returns:
            List[Book]: List of books matching the search criteria
        """
        pass


class TitleSearchStrategy(SearchStrategy):
    """Strategy for searching books by title"""

    def search(self, books: List[Book], query: str) -> List[Book]:
        query = query.lower()
        return [book for book in books if query in book.title.lower()]


class AuthorSearchStrategy(SearchStrategy):
    """Strategy for searching books by author"""

    def search(self, books: List[Book], query: str) -> List[Book]:
        query = query.lower()
        return [book for book in books if query in book.author.lower()]


class GenreSearchStrategy(SearchStrategy):
    """Strategy for searching books by genre"""

    def search(self, books: List[Book], query: str) -> List[Book]:
        query = query.lower()
        return [book for book in books if query in book.genre.lower()]


class YearSearchStrategy(SearchStrategy):
    """Strategy for searching books by publication year"""

    def search(self, books: List[Book], query: str) -> List[Book]:
        try:
            year = int(query)
            return [book for book in books if book.year == year]
        except ValueError:
            return []


class SearchContext:
    """Context class that manages the search strategies"""

    def __init__(self):
        self._strategies = {
            'title': TitleSearchStrategy(),
            'author': AuthorSearchStrategy(),
            'genre': GenreSearchStrategy(),
            'year': YearSearchStrategy()
        }

    def get_available_strategies(self) -> List[str]:
        """Get list of available search strategies"""
        return list(self._strategies.keys())

    def search(self, books: List[Book], strategy: str, query: str) -> List[Book]:
        """
        Perform search using specified strategy

        Args:
            books: List of books to search through
            strategy: Name of the search strategy to use
            query: Search query string

        Returns:
            List[Book]: List of books matching the search criteria

        Raises:
            ValueError: If the specified strategy doesn't exist
        """
        if strategy not in self._strategies:
            raise ValueError(f"Unknown search strategy: {strategy}")

        return self._strategies[strategy].search(books, query)


# Example usage:
"""
# Create search context
search_context = SearchContext()

# Get all available search strategies
strategies = search_context.get_available_strategies()
print(f"Available search strategies: {strategies}")

# Search by title
results = search_context.search(library.get_all_books(), 'title', 'Python')
print(f"Found {len(results)} books with 'Python' in the title")

# Search by author
results = search_context.search(library.get_all_books(), 'author', 'Martin')
print(f"Found {len(results)} books by authors containing 'Martin'")
"""