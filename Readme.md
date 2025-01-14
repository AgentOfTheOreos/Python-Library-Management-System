# Library Management System

A Python-based library management system featuring book inventory management, user authentication, borrowing operations, and advanced search capabilities.

## Table of Contents

- [Features](#features)
- [Design Patterns](#design-patterns)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)

## Features

### Book Management

- Add, remove, and update books in the inventory
- Track multiple copies of each book
- Monitor book availability and loan status
- Save book data in separate CSV files

### User Management

- User registration with secure password encryption
- User authentication system
- User data persistence in CSV format
- Role-based access control

### Borrowing System

- Book lending and return operations
- Automated waiting list management
- Real-time availability updates
- Loan history tracking

### Search and Display

- Multiple search strategies (title, author, genre, year)
- Support for partial matches
- Advanced filtering options
- Categorized book views

### Notifications

- Real-time notifications for book availability
- Waiting list position updates
- Loan confirmation notifications
- Return reminders

## Design Patterns

### 1. Strategy Pattern

- Implemented for flexible search functionality
- Different search strategies:
  - Title search
  - Author search
  - Genre search
  - Year search
- Easily extensible for new search types

### 2. Observer Pattern

- Used in the notification system
- Components:
  - NotificationCenter as the subject
  - UserNotificationObserver for individual users
  - BookNotificationManager for book-related events
- Real-time updates when:
  - Books become available
  - Waiting list positions change
  - Loans are processed

### 3. Decorator Pattern

- Enhances book objects with additional features
- Implemented decorators:
  - Digital version availability
  - Audio book features
  - Award winner status
  - Age recommendations

### 4. Factory Pattern

- BookFactory for creating book instances
- Handles:
  - Single book creation
  - Bulk book creation from CSV
  - Data validation
  - File persistence

### 5. Iterator Pattern

- Efficient navigation through book collections
- Different iteration strategies:
  - Chronological order
  - Alphabetical order
  - Genre-based grouping
  - Popularity-based sorting

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AgentOfTheOreos/Python-Library-Management-System
cd OOP_EX3_2025
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Running the Project

1. Ensure you're in the project root directory
2. Create required directories:

```bash
mkdir Data
```

3. Run the main application:

```bash
python main.py
```

4. The GUI will launch, allowing you to:
   - Register/Login
   - Manage books
   - Handle loans
   - Search and browse books
   - View notifications

## Usage

Below are two videos detailing the usage of the system:
- https://www.youtube.com/watch?v=yo06ppg90xo&t=411s
- https://www.youtube.com/watch?v=ElX185RIa5E

## Project Structure

```
├──library_system/
├── Data/
|   ├── avaliable_books.csv
│   ├── books.csv
|   ├── book_features.csv
|   ├── library.txt
|   ├── loaned_books.csv
│   └── users.csv
├── Library/
│   ├── __init__.py
│   ├── book.py
|   |── book_decorator.py
│   ├── book_factory.py
|   |── book_iterator.py
│   ├── user_management.py
│   ├── library_system.py
│   |── gui.py
|   |── notification.py
|   └── search.py 
├── tests/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_user.py
│   └── test_library.py
└── main.py

```

## Testing

Run all tests:

```bash
python -m unittest discover tests
```

Run specific test suite:

```bash
python -m unittest tests/test_book.py
python -m unittest tests/test_user.py
python -m unittest tests/test_library.py
```

---
