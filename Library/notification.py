from abc import ABC, abstractmethod
from typing import List, Dict, Set
from dataclasses import dataclass
from datetime import datetime


# Observer Pattern Interfaces
class Observer(ABC):
    """Abstract base class for observers"""

    @abstractmethod
    def update(self, notification: 'Notification') -> None:
        """Receive update from subject"""
        pass


class Subject(ABC):
    """Abstract base class for subjects"""

    def __init__(self):
        self._observers: Set[Observer] = set()

    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject"""
        self._observers.add(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject"""
        self._observers.discard(observer)

    def notify(self, notification: 'Notification') -> None:
        """Notify all observers"""
        for observer in self._observers:
            observer.update(notification)


@dataclass
class Notification:
    """Represents a notification in the system"""
    type: str  # e.g., 'BOOK_AVAILABLE', 'BOOK_DUE', 'WAITING_LIST_UPDATED'
    message: str
    timestamp: datetime
    book_title: str
    user: str


class NotificationCenter(Subject):
    """Central notification management system"""

    def __init__(self):
        super().__init__()
        self.notifications: Dict[str, List[Notification]] = {}  # username -> notifications

    def add_notification(self, notification: Notification) -> None:
        """Add a new notification and notify observers"""
        if notification.user not in self.notifications:
            self.notifications[notification.user] = []
        self.notifications[notification.user].append(notification)
        self.notify(notification)

    def get_user_notifications(self, username: str) -> List[Notification]:
        """Get all notifications for a specific user"""
        return self.notifications.get(username, [])

    def clear_user_notifications(self, username: str) -> None:
        """Clear all notifications for a specific user"""
        if username in self.notifications:
            self.notifications[username] = []


class UserNotificationObserver(Observer):
    """Handles notifications for a specific user"""

    def __init__(self, username: str):
        self.username = username
        self.unread_notifications: List[Notification] = []

    def update(self, notification: Notification) -> None:
        """Receive and process notifications"""
        if notification.user == self.username:
            self.unread_notifications.append(notification)

    def get_unread_notifications(self) -> List[Notification]:
        """Get all unread notifications"""
        notifications = self.unread_notifications.copy()
        self.unread_notifications.clear()
        return notifications


class BookNotificationManager:
    """Manages book-related notifications"""

    def __init__(self, notification_center: NotificationCenter):
        self.notification_center = notification_center

    def notify_book_available(self, book_title: str, user: str) -> None:
        """Notify user that a book is available"""
        print(f"Creating notification for {username} about {title}")  # Debug print
        notification = Notification(
            type='BOOK_AVAILABLE',
            message=f"The book '{title}' is now available for you to borrow",
            timestamp=datetime.now(),
            book_title=title,
            user=username
        )
        print("Adding notification to center")  # Debug print
        self.notification_center.add_notification(notification)

    def notify_book_due_soon(self, book_title: str, user: str, days_left: int) -> None:
        """Notify user about a book due date"""
        notification = Notification(
            type='BOOK_DUE',
            message=f"The book '{book_title}' is due in {days_left} days",
            timestamp=datetime.now(),
            book_title=book_title,
            user=user
        )
        self.notification_center.add_notification(notification)

    def notify_added_to_waiting_list(self, book_title: str, user: str, position: int) -> None:
        """Notify user they've been added to a waiting list"""
        notification = Notification(
            type='WAITING_LIST_UPDATED',
            message=f"You are number {position} in line for '{book_title}'",
            timestamp=datetime.now(),
            book_title=book_title,
            user=user
        )
        self.notification_center.add_notification(notification)
