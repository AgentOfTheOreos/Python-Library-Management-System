import unittest
from Library.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.valid_book = Book(
            title="Test Book",
            author="Test Author",
            copies=3,
            genre="Test Genre",
            year=2024
        )

    def test_book_creation(self):
        """Test basic book creation with valid parameters"""
        self.assertEqual(self.valid_book.title, "Test Book")
        self.assertEqual(self.valid_book.author, "Test Author")
        self.assertEqual(self.valid_book.copies, 3)
        self.assertEqual(self.valid_book.genre, "Test Genre")
        self.assertEqual(self.valid_book.year, 2024)
        self.assertEqual(self.valid_book.loaned_copies, 0)
        self.assertEqual(self.valid_book.total_borrows, 0)

    def test_invalid_book_creation(self):
        """Test book creation with invalid parameters"""
        # Test empty title
        with self.assertRaises(ValueError):
            Book(title="", author="Test Author", copies=3, genre="Test Genre", year=2024)

        # Test non-string title
        with self.assertRaises(ValueError):
            Book(title=123, author="Test Author", copies=3, genre="Test Genre", year=2024)

        # Test negative copies
        with self.assertRaises(ValueError):
            Book(title="Test Book", author="Test Author", copies=-1, genre="Test Genre", year=2024)

        # Test invalid genre
        with self.assertRaises(ValueError):
            Book(title="Test Book", author="Test Author", copies=3, genre="", year=2024)

        # Test non-integer year
        with self.assertRaises(ValueError):
            Book(title="Test Book", author="Test Author", copies=3, genre="Test Genre", year="2024")

    def test_loan_operations(self):
        """Test book loan and return operations"""
        # Test successful loan
        self.assertTrue(self.valid_book.loan())
        self.assertEqual(self.valid_book.loaned_copies, 1)
        self.assertEqual(self.valid_book.total_borrows, 1)

        # Test loan with all copies already loaned
        book = Book(title="Test", author="Test", copies=1, genre="Test", year=2024)
        book.loan()
        self.assertFalse(book.loan())  # Should fail as no copies available

        # Test return
        self.assertTrue(book.return_book())
        self.assertEqual(book.loaned_copies, 0)

        # Test return when no copies are loaned
        self.assertFalse(book.return_book())

    def test_availability_properties(self):
        """Test availability-related properties"""
        # Test available_copies property
        self.assertEqual(self.valid_book.available_copies, 3)
        self.valid_book.loan()
        self.assertEqual(self.valid_book.available_copies, 2)

        # Test is_available property
        self.assertTrue(self.valid_book.is_available)
        book = Book(title="Test", author="Test", copies=1, genre="Test", year=2024)
        book.loan()
        self.assertFalse(book.is_available)

        # Test is_fully_loaned property
        self.assertFalse(self.valid_book.is_fully_loaned)
        self.assertTrue(book.is_fully_loaned)

    def test_update_copies(self):
        """Test updating the number of copies"""
        # Test valid update
        self.valid_book.update_copies(5)
        self.assertEqual(self.valid_book.copies, 5)

        # Test update with negative number
        with self.assertRaises(ValueError):
            self.valid_book.update_copies(-1)

        # Test update with number less than loaned copies
        self.valid_book.loan()  # Loan one copy
        with self.assertRaises(ValueError):
            self.valid_book.update_copies(0)  # Should fail as one copy is loaned

    def test_dictionary_conversion(self):
        """Test conversion to and from dictionary format"""
        # Test to_dict()
        book_dict = self.valid_book.to_dict()
        self.assertEqual(book_dict['title'], "Test Book")
        self.assertEqual(book_dict['author'], "Test Author")
        self.assertEqual(book_dict['is_loaned'], "No")
        self.assertEqual(book_dict['copies'], 3)
        self.assertEqual(book_dict['genre'], "Test Genre")
        self.assertEqual(book_dict['year'], 2024)

        # Test from_dict()
        new_book = Book.from_dict(book_dict)
        self.assertEqual(new_book.title, self.valid_book.title)
        self.assertEqual(new_book.author, self.valid_book.author)
        self.assertEqual(new_book.copies, self.valid_book.copies)
        self.assertEqual(new_book.genre, self.valid_book.genre)
        self.assertEqual(new_book.year, self.valid_book.year)


if __name__ == '__main__':
    unittest.main()
