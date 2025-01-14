import csv
from typing import List, Dict, Set, Optional, Any
from collections import defaultdict
import logging
from datetime import datetime
from .book import Book
from .book_factory import BookFactory
from .user_management import UserManager
from .search import SearchContext
from .notification import (NotificationCenter,
                           BookNotificationManager,
                           UserNotificationObserver,
                           Notification)
from .book_iterator import (BookIterator,
                            ChronologicalIterator,
                            AlphabeticalIterator,
                            GenreIterator,
                            PopularityIterator,
                            AvailabilityIterator)


class LibrarySystem:
    """Core library management system handling books, loans, and waiting lists"""

    def __init__(self, books_file: str = 'Data/books.csv',
                 available_books_file: str = 'Data/available_books.csv',
                 loaned_books_file: str = 'Data/loaned_books.csv',
                 log_file: str = 'Data/library.txt',
                 features_file: str = 'Data/book_features.csv'):
        """
        Initialize the LibrarySystem instance.

        Args:
            books_file (str): Path to the file containing all books.
            available_books_file (str): Path to the file for available books.
            loaned_books_file (str): Path to the file for loaned books.
            log_file (str): Path to the log file.
        """
        # Initialize file paths
        self.features_file = features_file
        self.book_features = {}
        self._load_features()
        self.books_file = books_file
        self.available_books_file = available_books_file
        self.loaned_books_file = loaned_books_file

        # Set up logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

        # Initialize data structures
        self.books: Dict[str, Book] = {}  # title -> Book
        self.waiting_lists: Dict[str, List[str]] = defaultdict(list)  # title -> list of usernames
        self.user_loans: Dict[str, Set[str]] = defaultdict(set)  # username -> set of book titles

        # Initialize search context
        self.search_context = SearchContext()

        # Initialize notification system
        self.notification_center = NotificationCenter()
        self.book_notification_manager = BookNotificationManager(self.notification_center)

        # Load initial data
        self._load_books()

    def _get_book_case_insensitive(self, title: str) -> Optional[Book]:
        """
        Find a book by title, ignoring case.

        Args:
            title (str): The title to search for.

        Returns:
            Optional[Book]: The book instance if found, or None otherwise.
        """
        title_lower = title.lower()
        for book_title, book in self.books.items():
            if book_title.lower() == title_lower:
                return book
        return None

    def register_user_for_notifications(self, username: str) -> None:
        """
        Register a user to receive notifications.

        Args:
            username (str): Username of the user to register.
        """
        # Check if user already has an observer
        for observer in self.notification_center._observers:
            if isinstance(observer, UserNotificationObserver) and observer.username == username:
                print(f"User {username} already has an observer")
                return

        print(f"Creating new observer for {username}")
        observer = UserNotificationObserver(username)
        self.notification_center.attach(observer)
        print(f"Current observers: {len(self.notification_center._observers)}")

    def unregister_user_from_notifications(self, username: str) -> None:
        """
        Unregister a user from receiving notifications.

        Args:
            username (str): Username of the user to unregister.
        """
        # Find and remove the user's observer
        for observer in self.notification_center._observers:
            if isinstance(observer, UserNotificationObserver) and observer.username == username:
                self.notification_center.detach(observer)
                break

    def _load_books(self) -> None:
        """Load books from CSV files"""
        try:
            books = BookFactory.create_from_csv(self.books_file)
            for book in books:
                self.books[book.title] = book
            self._log_operation("Books loaded successfully")
        except Exception as e:
            self._log_operation(f"Failed to load books: {str(e)}", is_error=True)
            raise

    def _save_books(self) -> None:
        """Save books to all necessary CSV files"""
        try:
            # Save all books
            BookFactory.save_to_csv(list(self.books.values()), self.books_file)

            # Save available books
            available_books = [book for book in self.books.values() if book.available_copies > 0]
            BookFactory.save_to_csv(available_books, self.available_books_file)

            # Save loaned books
            loaned_books = [book for book in self.books.values() if book.loaned_copies > 0]
            BookFactory.save_to_csv(loaned_books, self.loaned_books_file)

            self._log_operation("Books saved successfully")
        except Exception as e:
            self._log_operation(f"Failed to save books: {str(e)}", is_error=True)
            raise

    @staticmethod
    def _log_operation(message: str, is_error: bool = False) -> None:
        """
        Internal method to log an operation to the log file.

        Args:
            message (str): The message to log.
            is_error (bool): If True, log as an error. Defaults to False.
        """
        if is_error:
            logging.error(message)
        else:
            logging.info(message)

    def add_book(self, title: str, author: str, copies: int, genre: str, year: int) -> bool:
        """
        Add a new book to the library.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            copies (int): Number of copies.
            genre (str): Genre of the book.
            year (int): Year of publication.

        Returns:
            bool: True if the book was added successfully, False otherwise.
        """
        try:
            if title in self.books:
                book = self.books[title]
                book.update_copies(book.copies + copies)
            else:
                book = BookFactory.create_book(title, author, copies, genre, year)
                self.books[title] = book

            self._save_books()
            self._log_operation(f"Book added successfully: {title}")
            return True
        except Exception as e:
            self._log_operation(f"Book added fail: {title}: {str(e)}", is_error=True)
            return False

    def remove_book(self, title: str) -> bool:
        """
        Remove a book from the library.

        Args:
            title (str): Title of the book to remove.

        Returns:
            bool: True if the book was removed successfully, False otherwise.
        """
        try:
            if title not in self.books:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            if self.books[title].loaned_copies > 0:
                self._log_operation(f"Cannot remove book {title} - copies are still on loan", is_error=True)
                return False

            del self.books[title]
            self._save_books()
            self._log_operation(f"Book removed successfully: {title}")
            return True
        except Exception as e:
            self._log_operation(f"Failed to remove book {title}: {str(e)}", is_error=True)
            return False

    def loan_book(self, title: str, username: str) -> bool:
        """
        Loan a book to a user.

        Args:
            title (str): Title of the book to loan.
            username (str): Username of the user borrowing the book.

        Returns:
            bool: True if the book was loaned successfully, False otherwise.
        """
        try:
            book = self._get_book_case_insensitive(title)
            if not book:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            if not book.is_available:
                # Debug prints
                print(f"Book {title} not available, adding {username} to waiting list")

                # Add user to waiting list if not already in it
                if username not in self.waiting_lists[book.title]:
                    waiting_position = len(self.waiting_lists[book.title]) + 1
                    self.waiting_lists[book.title].append(username)
                    self._log_operation(f"Added {username} to waiting list for {book.title}")

                    # Debug prints
                    print(f"Added to waiting list. Current list: {self.waiting_lists[book.title]}")

                    # Notify user about their position
                    self.book_notification_manager.notify_added_to_waiting_list(
                        book.title, username, waiting_position
                    )

                    # Register user for notifications if not already registered
                    self.register_user_for_notifications(username)
                return False

            # Process the loan
            if book.loan():
                self.user_loans[username].add(book.title)
                self._save_books()
                self._log_operation(f"Book borrowed successfully: {book.title} by {username}")
                return True

            return False
        except Exception as e:
            self._log_operation(f"Failed to loan book {title}: {str(e)}", is_error=True)
            return False

    def return_book(self, title: str, username: str) -> bool:
        """
        Return a loaned book and notify the next user in the waiting list.

        Args:
            title (str): Title of the book to return.
            username (str): Username of the user returning the book.

        Returns:
            bool: True if the book was returned successfully, False otherwise.
        """
        try:
            book = self._get_book_case_insensitive(title)
            if not book:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            if title not in self.user_loans[username]:
                self._log_operation(f"Book {title} not loaned to {username}", is_error=True)
                return False

            if book.return_book():
                self.user_loans[username].remove(title)
                self._save_books()
                self._log_operation(f"Book returned successfully: {title} by {username}")

                print(f"Book returned: {title}")
                print(f"Checking waiting list for {title}")
                print(f"Current waiting list before notification: {self.waiting_lists[book.title]}")

                # Notify next user in waiting list
                if self.waiting_lists[book.title]:
                    next_user = self.waiting_lists[book.title][0]
                    print(f"Notifying next user: {next_user}")
                    # Create notification for book availability
                    notification = Notification(
                        type='BOOK_AVAILABLE',
                        message=f"The book '{title}' is now available for you to borrow",
                        timestamp=datetime.now(),
                        book_title=title,
                        user=next_user
                    )
                    self.notification_center.add_notification(notification)
                    # Remove user from waiting list after notification
                    self.waiting_lists[book.title].pop(0)
                    self._log_operation(f"Notified {next_user} that {title} is available")

                return True

            return False
        except Exception as e:
            self._log_operation(f"Failed to return book {title}: {str(e)}", is_error=True)
            print(f"Error in return_book: {str(e)}")
            return False

    def update_book(self, title: str, updates: dict) -> bool:
        """
        Update book details

        Args:
            title: Title of the book to update
            updates: Dictionary containing the fields to update and their new values

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            book = self._get_book_case_insensitive(title)
            if not book:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            # Validate updates
            if 'copies' in updates and updates['copies'] < book.loaned_copies:
                self._log_operation("Cannot reduce copies below number of loaned copies", is_error=True)
                return False

            # Apply updates
            if 'title' in updates and updates['title'] != book.title:
                # Handle title change (needs special care as it's the key in self.books)
                new_title = updates['title']
                if new_title in self.books and new_title.lower() != title.lower():
                    self._log_operation(f"Book with title '{new_title}' already exists", is_error=True)
                    return False
                del self.books[book.title]
                book.title = new_title
                self.books[new_title] = book

            if 'author' in updates:
                book.author = updates['author']
            if 'genre' in updates:
                book.genre = updates['genre']
            if 'year' in updates:
                book.year = updates['year']
            if 'copies' in updates:
                book.update_copies(updates['copies'])

            self._save_books()
            self._log_operation(f"Book '{title}' updated successfully")
            return True

        except Exception as e:
            self._log_operation(f"Failed to update book {title}: {str(e)}", is_error=True)
            return False

    def _load_features(self) -> None:
        """Load book features from CSV"""
        try:
            with open(self.features_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.book_features[row['book_title']] = row['features'].split(',')
        except FileNotFoundError:
            # Create file if it doesn't exist
            self._save_features()

    def _save_features(self) -> None:
        """Save book features to CSV"""
        with open(self.features_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['book_title', 'features'])
            writer.writeheader()
            for title, features in self.book_features.items():
                if features:
                    writer.writerow({
                        'book_title': title,
                        'features': ','.join(features)
                    })

    def update_book_features(self, title: str, features: List[str]) -> bool:
        """Update features for a book"""
        try:
            if title in self.books:
                if features:
                    self.book_features[title] = features
                else:
                    # Remove empty feature lists
                    self.book_features.pop(title, None)
                self._save_features()
                self._log_operation(f"Updated features for book: {title}")
                return True
            self._log_operation(f"Failed to update features: book {title} not found", is_error=True)
            return False
        except Exception as e:
            self._log_operation(f"Error updating features: {str(e)}", is_error=True)
            return False

    def get_book_features(self, title: str) -> List[str]:
        """Get features for a book"""
        return self.book_features.get(title, [])

    def add_to_waiting_list(self, title: str, username: str) -> bool:
        """
        Add a user to a book's waiting list

        Args:
            title: Book title
            username: Username to add to waiting list

        Returns:
            bool: True if added successfully, False otherwise
        """
        try:
            book = self._get_book_case_insensitive(title)
            if not book:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            # Check if user is already in waiting list
            if username in self.waiting_lists[book.title]:
                self._log_operation(f"User {username} is already in waiting list for {book.title}", is_error=True)
                return False

            # Add to waiting list
            waiting_position = len(self.waiting_lists[book.title]) + 1
            self.waiting_lists[book.title].append(username)
            self._log_operation(f"Added {username} to waiting list for {book.title}")

            # Notify user about their position
            self.book_notification_manager.notify_added_to_waiting_list(
                book.title, username, waiting_position
            )
            return True

        except Exception as e:
            self._log_operation(f"Failed to add to waiting list: {str(e)}", is_error=True)
            return False

    def remove_from_waiting_list(self, title: str, username: str) -> bool:
        """
        Remove a user from a book's waiting list

        Args:
            title: Book title
            username: Username to remove from waiting list

        Returns:
            bool: True if removed successfully, False otherwise
        """
        try:
            book = self._get_book_case_insensitive(title)
            if not book:
                self._log_operation(f"Book not found: {title}", is_error=True)
                return False

            if username in self.waiting_lists[book.title]:
                self.waiting_lists[book.title].remove(username)
                self._log_operation(f"Removed {username} from waiting list for {book.title}")
                return True

            self._log_operation(f"User {username} not found in waiting list for {book.title}", is_error=True)
            return False

        except Exception as e:
            self._log_operation(f"Failed to remove from waiting list: {str(e)}", is_error=True)
            return False

    def get_user_waiting_list_positions(self, username: str) -> dict:
        """
        Get all books a user is waiting for and their position in each waiting list

        Args:
            username: Username to check

        Returns:
            dict: Dictionary mapping book titles to waiting list positions
        """
        positions = {}
        for title, waiting_list in self.waiting_lists.items():
            if username in waiting_list:
                positions[title] = waiting_list.index(username) + 1
        return positions

    def notify_next_in_line(self, title: str) -> bool:
        """
        Notify the next user in line that a book is available

        Args:
            title: Book title

        Returns:
            bool: True if someone was notified, False if no one is waiting
        """
        book = self._get_book_case_insensitive(title)
        if not book:
            return False

        waiting_list = self.waiting_lists.get(book.title, [])
        if waiting_list:
            next_user = waiting_list[0]
            self.book_notification_manager.notify_book_available(book.title, next_user)
            return True
        return False

    def get_user_loans(self, username: str) -> List[str]:
        """Get list of books currently loaned to a user"""
        return list(self.user_loans[username])

    def get_waiting_list(self, title: str) -> List[str]:
        """Get the waiting list for a book"""
        return self.waiting_lists.get(title, [])

    def get_available_books(self) -> List[Book]:
        """Get list of all available books"""
        return [book for book in self.books.values() if book.available_copies > 0]

    def get_loaned_books(self) -> List[Book]:
        """Get list of all books that have at least one copy loaned"""
        return [book for book in self.books.values() if book.loaned_copies > 0]

    def get_all_books(self) -> List[Book]:
        """Get list of all books"""
        return list(self.books.values())

    @staticmethod
    def configure_iterator(iterator_type: str, **kwargs) -> Dict[str, Any]:
        """
        Configure additional arguments for specific iterator types.
        Args:
            iterator_type: The type of iterator.
            **kwargs: Additional keyword arguments (e.g., reverse, by_author).

        Returns:
            A dictionary of configuration arguments for the iterator.
        """
        if iterator_type == 'chronological':
            return {'reverse': kwargs.get('reverse', False)}
        elif iterator_type == 'alphabetical':
            return {'by_author': kwargs.get('by_author', False)}
        elif iterator_type == 'availability':
            return {'available_only': kwargs.get('available_only', True)}
        elif iterator_type == 'genre':
            return {}
        elif iterator_type == 'popularity':
            return {}
        else:
            raise ValueError(f"Unknown iterator type: {iterator_type}")

    def get_iterator(self, iterator_type: str, **kwargs) -> BookIterator:
        """
        Get a specific type of book iterator.

        Args:
            iterator_type: Type of iterator.
            **kwargs: Additional arguments for specific iterators.

        Returns:
            BookIterator: The requested iterator.
        """
        books = list(self.books.values())
        config = self.configure_iterator(iterator_type, **kwargs)

        if iterator_type == 'chronological':
            return ChronologicalIterator(books, **config)
        elif iterator_type == 'alphabetical':
            return AlphabeticalIterator(books, **config)
        elif iterator_type == 'genre':
            return GenreIterator(books)
        elif iterator_type == 'popularity':
            return PopularityIterator(books, self)
        elif iterator_type == 'availability':
            return AvailabilityIterator(books, **config)
        else:
            raise ValueError(f"Unknown iterator type: {iterator_type}")

    def search_books(self, strategy: str, query: str) -> List[Book]:
        """
        Search for books using specified strategy

        Args:
            strategy: Search strategy to use ('title', 'author', 'genre', 'year')
            query: Search query string

        Returns:
            List[Book]: List of books matching the search criteria
        """
        try:
            search_context = SearchContext()
            results = search_context.search(self.get_all_books(), strategy, query)
            self._log_operation(f"Search {strategy}='{query}' completed successfully")
            return results
        except Exception as e:
            self._log_operation(f"Search failed for {strategy}='{query}': {str(e)}", is_error=True)
            raise
