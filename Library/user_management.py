from dataclasses import dataclass
import csv
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class User:
    """Represents a user in the library system"""
    username: str
    password_hash: str

    @classmethod
    def create(cls, username: str, password: str) -> 'User':
        """Create a new user with encrypted password"""
        password_hash = generate_password_hash(password)
        return cls(username=username, password_hash=password_hash)

    def verify_password(self, password: str) -> bool:
        """Verify if the given password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Convert user to dictionary format for CSV storage"""
        return {
            'username': self.username,
            'password_hash': self.password_hash
        }


class UserManager:
    """Manages user operations including registration, authentication, and storage"""

    def __init__(self, users_file: str = 'Data/users.csv'):
        self.users_file = users_file
        self.users: dict[str, User] = {}
        self._load_users()

    def _load_users(self) -> None:
        """Load users from CSV file"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(
                        username=row['username'],
                        password_hash=row['password_hash']
                    )
                    self.users[user.username] = user
        except FileNotFoundError:
            # Create the file if it doesn't exist
            self._save_users()

    def _save_users(self) -> None:
        """Save users to CSV file"""
        with open(self.users_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['username', 'password_hash'])
            writer.writeheader()
            for user in self.users.values():
                writer.writerow(user.to_dict())

    def register(self, username: str, password: str) -> bool:
        """
        Register a new user
        Returns True if successful, False if username already exists
        """
        if not username or not password:
            raise ValueError("Username and password cannot be empty")

        if username in self.users:
            return False

        user = User.create(username, password)
        self.users[username] = user
        self._save_users()
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user
        Returns True if credentials are valid, False otherwise
        """
        user = self.users.get(username)
        if not user:
            return False
        return user.verify_password(password)

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.users.get(username)

    def get_all_users(self) -> List[str]:
        """Get list of all usernames"""
        return list(self.users.keys())

    def delete_user(self, username: str) -> bool:
        """
        Delete a user
        Returns True if successful, False if user doesn't exist
        """
        if username not in self.users:
            return False
        del self.users[username]
        self._save_users()
        return True
