from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime


class BookInterface(ABC):
    """
    Abstract interface for all books and decorators.
    Defines the common properties and methods that any book-related class must implement.
    """
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get full book description with all features"""
        pass

    @property
    @abstractmethod
    def special_features(self) -> List[str]:
        """Get list of special features"""
        pass


class BookDecorator(BookInterface):
    """
    Base decorator class for enhancing books with additional features.
    Implements the `BookInterface` and wraps an existing book object.
    """
    def __init__(self, book: BookInterface):
        self._book = book

    @property
    def title(self) -> str:
        return self._book.title

    @property
    def author(self) -> str:
        return self._book.author

    @property
    def description(self) -> str:
        return self._book.description

    @property
    def special_features(self) -> List[str]:
        return self._book.special_features


class DigitalVersionDecorator(BookDecorator):
    """
    Adds a digital version feature to a book, including supported formats.
    """
    def __init__(self, book: BookInterface, format_types: List[str] = None):
        super().__init__(book)
        self._formats = format_types or ["PDF", "EPUB"]

    @property
    def description(self) -> str:
        return f"{self._book.description}\nAvailable in digital formats: {', '.join(self._formats)}"

    @property
    def special_features(self) -> List[str]:
        return self._book.special_features + [f"Digital Version ({', '.join(self._formats)})"]


class AudioBookDecorator(BookDecorator):
    """
    Adds audiobook features, including narrator and duration.
    """
    def __init__(self, book: BookInterface, narrator: str, duration_hours: float):
        super().__init__(book)
        self.narrator = narrator
        self.duration_hours = duration_hours

    @property
    def description(self) -> str:
        return f"{self._book.description}\nAudiobook narrated by {self.narrator} ({self.duration_hours} hours)"

    @property
    def special_features(self) -> List[str]:
        return self._book.special_features + [f"Audiobook ({self.duration_hours}h)"]


class AwardWinnerDecorator(BookDecorator):
    """
    Adds award information to a book.
    """
    def __init__(self, book: BookInterface, award_name: str, year: int):
        super().__init__(book)
        self.award_name = award_name
        self.award_year = year

    @property
    def description(self) -> str:
        return f"{self._book.description}\n{self.award_name} Winner ({self.award_year})"

    @property
    def special_features(self) -> List[str]:
        return self._book.special_features + [f"{self.award_name} ({self.award_year})"]


class BestsellerDecorator(BookDecorator):
    """
    Adds bestseller status to a book.
    """
    def __init__(self, book: BookInterface, list_name: str = "New York Times"):
        super().__init__(book)
        self.list_name = list_name

    @property
    def description(self) -> str:
        return f"{self._book.description}\n{self.list_name} Bestseller"

    @property
    def special_features(self) -> List[str]:
        return self._book.special_features + [f"{self.list_name} Bestseller"]


class AgeRecommendationDecorator(BookDecorator):
    """
    Adds age recommendation details to a book.
    """
    def __init__(self, book: BookInterface, min_age: int, max_age: Optional[int] = None):
        super().__init__(book)
        self.min_age = min_age
        self.max_age = max_age

    @property
    def description(self) -> str:
        if self.max_age:
            age_range = f"{self.min_age}-{self.max_age}"
        else:
            age_range = f"{self.min_age}+"
        return f"{self._book.description}\nRecommended Age: {age_range} years"

    @property
    def special_features(self) -> List[str]:
        if self.max_age:
            age_range = f"{self.min_age}-{self.max_age}"
        else:
            age_range = f"{self.min_age}+"
        return self._book.special_features + [f"Age Range: {age_range}"]


# Example usage:
"""
# Create a basic book
book = Book("The Hobbit", "J.R.R. Tolkien", 5, "Fantasy", 1937)

# Add digital version
digital_book = DigitalVersionDecorator(book, ["PDF", "EPUB", "MOBI"])

# Add audiobook feature
audio_digital_book = AudioBookDecorator(digital_book, "Andy Sarkis", 11.5)

# Add award information
award_audio_digital_book = AwardWinnerDecorator(
    audio_digital_book, "Hugo Award", 1938
)

# The final book now has all features
print(award_audio_digital_book.description)
print("\nSpecial Features:")
for feature in award_audio_digital_book.special_features:
    print(f"- {feature}")
"""