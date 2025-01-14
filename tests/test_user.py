import unittest
import os
from Library.user_management import UserManager


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create test directory in the 'Data' folder
        self.test_dir = "Data/test"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Use a test-specific CSV file
        self.test_users_file = os.path.join(self.test_dir, "test_users.csv")

        # Initialize UserManager with test file
        self.user_manager = UserManager(users_file=self.test_users_file)

        # Test credentials
        self.test_username = "testuser"
        self.test_password = "testpass123"

    def tearDown(self):
        """Clean up after each test method"""
        # Remove test file
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)
        # Remove test directory
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        # Remove parent test directory if empty
        parent_dir = os.path.dirname(self.test_dir)
        if os.path.exists(parent_dir) and not os.listdir(parent_dir):
            os.rmdir(parent_dir)

    def test_user_registration(self):
        """Test user registration functionality"""
        # Test successful registration
        self.assertTrue(
            self.user_manager.register(self.test_username, self.test_password),
            "User registration should succeed with valid credentials"
        )

        # Test duplicate registration
        self.assertFalse(
            self.user_manager.register(self.test_username, "differentpass"),
            "Duplicate registration should fail"
        )

        # Test registration with empty username
        try:
            self.user_manager.register("", self.test_password)
            self.fail("Should have raised ValueError")
        except ValueError as e:
            self.assertEqual(
                str(e),
                "Username and password cannot be empty",
                "Wrong error message"
            )

        # Test registration with empty password
        try:
            self.user_manager.register(self.test_username, "")
            self.fail("Should have raised ValueError")
        except ValueError as e:
            self.assertEqual(
                str(e),
                "Username and password cannot be empty",
                "Wrong error message"
            )

    def test_user_authentication(self):
        """Test user authentication functionality"""
        # Register a test user first
        self.user_manager.register(self.test_username, self.test_password)

        # Test successful authentication
        self.assertTrue(
            self.user_manager.authenticate(self.test_username, self.test_password),
            "Authentication should succeed with correct credentials"
        )

        # Test failed authentication cases
        self.assertFalse(
            self.user_manager.authenticate(self.test_username, "wrongpass"),
            "Authentication should fail with incorrect password"
        )
        self.assertFalse(
            self.user_manager.authenticate("nonexistent", self.test_password),
            "Authentication should fail with nonexistent user"
        )
        self.assertFalse(
            self.user_manager.authenticate("", ""),
            "Authentication should fail with empty credentials"
        )

    def test_password_security(self):
        """Test password security features"""
        # Register a user
        self.user_manager.register(self.test_username, self.test_password)

        # Get the stored user data
        stored_user = self.user_manager.get_user(self.test_username)

        # Verify password is not stored in plain text
        self.assertNotEqual(
            stored_user.password_hash,
            self.test_password,
            "Password should not be stored in plain text"
        )

        # Verify different passwords generate different hashes
        self.user_manager.register("user2", "pass1")
        self.user_manager.register("user3", "pass2")
        user2 = self.user_manager.get_user("user2")
        user3 = self.user_manager.get_user("user3")
        self.assertNotEqual(
            user2.password_hash,
            user3.password_hash,
            "Different passwords should generate different hashes"
        )

    def test_user_data_persistence(self):
        """Test if user data is properly persisted to CSV"""
        # Register multiple users
        test_users = [
            ("user1", "pass1"),
            ("user2", "pass2"),
            ("user3", "pass3")
        ]

        for username, password in test_users:
            self.user_manager.register(username, password)

        # Create new UserManager instance to read from file
        new_manager = UserManager(self.test_users_file)

        # Verify all users were properly saved and can be loaded
        for username, password in test_users:
            self.assertTrue(
                new_manager.authenticate(username, password),
                f"User {username} should be retrievable after persistence"
            )

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Register multiple users
        test_users = ["user1", "user2", "user3"]
        for username in test_users:
            self.user_manager.register(username, "password")

        # Get all users
        all_users = self.user_manager.get_all_users()

        # Verify all registered users are present
        for username in test_users:
            self.assertIn(
                username,
                all_users,
                f"User {username} should be in the list of all users"
            )

        # Verify count matches
        self.assertEqual(
            len(all_users),
            len(test_users),
            "Number of users should match number registered"
        )


if __name__ == '__main__':
    unittest.main()
