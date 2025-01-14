import unittest
import os
from Library.library_system import LibrarySystem
from Library.book import Book
import logging


class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create test directory in the Data folder
        self.test_dir = "Data/test"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Test file paths
        self.test_books_file = os.path.join(self.test_dir, "test_books.csv")
        self.test_available_file = os.path.join(self.test_dir, "test_available_books.csv")
        self.test_loaned_file = os.path.join(self.test_dir, "test_loaned_books.csv")
        self.test_log_file = os.path.join(self.test_dir, "test_library.txt")

        # Initialize the test books file with an empty CSV
        with open(self.test_books_file, 'w', encoding='utf-8') as f:
            f.write("title,author,is_loaned,copies,genre,year\n")

        # Initialize library system with test files
        self.library = LibrarySystem(
            books_file=self.test_books_file,
            available_books_file=self.test_available_file,
            loaned_books_file=self.test_loaned_file,
            log_file=self.test_log_file
        )

        # Sample book data for tests
        self.test_book_data = {
            'title': "Test Book",
            'author': "Test Author",
            'copies': 3,
            'genre': "Test Genre",
            'year': 2024
        }

    def tearDown(self):
        """Clean up after each test method"""
        # Close any open log file handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
            handler.close()

        # Remove test files
        test_files = [
            self.test_books_file,
            self.test_available_file,
            self.test_loaned_file,
            self.test_log_file
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

        # Remove test directory if empty
        if os.path.exists(self.test_dir) and not os.listdir(self.test_dir):
            os.rmdir(self.test_dir)
            parent_dir = os.path.dirname(self.test_dir)
            if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                os.rmdir(parent_dir)

    def test_add_book(self):
        """Test adding books to the library"""
        # Test adding a new book
        self.assertTrue(
            self.library.add_book(**self.test_book_data),
            "Should successfully add a new book"
        )

        # Verify book was added
        books = self.library.get_all_books()
        self.assertEqual(len(books), 1, "Should have exactly one book")
        book = books[0]
        for key, value in self.test_book_data.items():
            self.assertEqual(getattr(book, key), value)

    def test_remove_book(self):
        """Test removing books from the library"""
        # Add a book first
        self.library.add_book(**self.test_book_data)

        # Test successful removal
        self.assertTrue(
            self.library.remove_book(self.test_book_data['title']),
            "Should successfully remove existing book"
        )

        # Verify book was removed
        self.assertEqual(len(self.library.get_all_books()), 0)

        # Test removing non-existent book
        self.assertFalse(
            self.library.remove_book("Nonexistent Book"),
            "Should fail to remove non-existent book"
        )

    def test_loan_operations(self):
        """Test book loan and return operations"""
        # Add a test book
        self.library.add_book(**self.test_book_data)
        test_user = "test_user"

        # Test successful loan
        self.assertTrue(
            self.library.loan_book(self.test_book_data['title'], test_user),
            "Should successfully loan available book"
        )

        # Verify loan status
        book = self.library._get_book_case_insensitive(self.test_book_data['title'])
        self.assertEqual(book.loaned_copies, 1)
        self.assertIn(test_user, self.library.user_loans)

        # Test successful return
        self.assertTrue(
            self.library.return_book(self.test_book_data['title'], test_user),
            "Should successfully return loaned book"
        )

        # Verify return status
        self.assertEqual(book.loaned_copies, 0)
        self.assertNotIn(self.test_book_data['title'], self.library.user_loans[test_user])

    def test_waiting_list(self):
        """Test waiting list functionality"""
        # Add a book with 1 copy
        book_data = self.test_book_data.copy()
        book_data['copies'] = 1
        self.library.add_book(**book_data)

        # Loan the only copy
        self.library.loan_book(book_data['title'], "user1")

        # Try to loan to another user
        self.assertFalse(
            self.library.loan_book(book_data['title'], "user2"),
            "Should fail to loan book with no copies available"
        )

        # Verify user2 is in waiting list before return
        waiting_list = self.library.get_waiting_list(book_data['title'])
        self.assertIn("user2", waiting_list, "User should be in waiting list before book return")

        # Return the book
        self.library.return_book(book_data['title'], "user1")

        # Verify waiting list is empty (as user gets automatically removed and notified)
        waiting_list = self.library.get_waiting_list(book_data['title'])
        self.assertEqual(
            len(waiting_list),
            0,
            "Waiting list should be empty after return as user is automatically removed and notified"
        )

        # Verify the book is available
        book = self.library._get_book_case_insensitive(book_data['title'])
        self.assertTrue(
            book.is_available,
            "Book should be available after return"
        )

    def test_get_available_books(self):
        """Test retrieving available books"""
        # Add two books with different availability
        self.library.add_book(**self.test_book_data)  # 3 copies
        self.library.add_book(
            title="Test Book 2",
            author="Test Author",
            copies=1,
            genre="Test Genre",
            year=2024
        )

        # Loan one book fully
        self.library.loan_book("Test Book 2", "user1")

        # Check available books
        available_books = self.library.get_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0].title, self.test_book_data['title'])

    def test_search_functionality(self):
        """Test book search functionality"""
        # Add test books
        self.library.add_book(**self.test_book_data)
        self.library.add_book(
            title="Another Test",
            author="Different Author",
            copies=2,
            genre="Different Genre",
            year=2023
        )

        # Test search by title
        results = self.library.search_books('title', 'Test')
        self.assertEqual(len(results), 2)

        # Test search by author
        results = self.library.search_books('author', 'Different')
        self.assertEqual(len(results), 1)

        # Test search by genre
        results = self.library.search_books('genre', 'Test Genre')
        self.assertEqual(len(results), 1)

        # Test search with no results
        results = self.library.search_books('title', 'Nonexistent')
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
