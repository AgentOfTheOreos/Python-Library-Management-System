import tkinter as tk
from typing import List
from tkinter import ttk, messagebox
from typing import Optional
from .library_system import LibrarySystem
from .user_management import UserManager
from .notification import UserNotificationObserver
from .book_iterator import GenreIterator
from .book import Book


class LibraryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")

        # Configure window
        self.root.configure(bg="#ecf0f1")  # Set background color

        # Configure styles
        self.style = self._configure_styles()

        # Initialize systems
        self.library = LibrarySystem()
        self.user_manager = UserManager()

        # Track current user
        self.current_user: Optional[str] = None

        # Create main frame with styling
        self.main_frame = ttk.Frame(self.root, padding="20", style='Main.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Start with login screen
        self.show_login_screen()

    def _clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _configure_styles(self):
        """Configure ttk styles for the application"""
        # Create style object
        style = ttk.Style(self.root)

        # Set theme
        style.theme_use('clam')  # 'clam' is a good base theme for customization

        # Define colors
        primary_color = "#2c3e50"  # Dark blue-gray
        secondary_color = "#3498db"  # Bright blue
        accent_color = "#e74c3c"  # Red for important actions
        bg_color = "#ecf0f1"  # Light gray
        text_color = "#2c3e50"  # Dark blue-gray

        # Configure common elements
        style.configure('.',  # Default style
                        background=bg_color,
                        foreground=text_color,
                        font=('Helvetica', 10)
                        )

        # Main buttons style
        style.configure('Main.TButton',
                        font=('Helvetica', 11),
                        padding=10,
                        background=secondary_color,
                        relief='raised'
                        )
        style.map('Main.TButton',
                  background=[('active', '#2980b9'), ('pressed', '#2980b9')],
                  relief=[('pressed', 'sunken')]
                  )

        # Action buttons (like Submit, Save, etc.)
        style.configure('Action.TButton',
                        font=('Helvetica', 10, 'bold'),
                        padding=8,
                        background=accent_color
                        )

        # Labels
        style.configure('Title.TLabel',
                        font=('Helvetica', 16, 'bold'),
                        foreground=primary_color,
                        padding=10
                        )

        style.configure('Subtitle.TLabel',
                        font=('Helvetica', 12),
                        foreground=primary_color,
                        padding=5
                        )

        # Frames
        style.configure('Main.TFrame',
                        background=bg_color,
                        relief='flat'
                        )

        # Notebook (tabbed interface)
        style.configure('TNotebook',
                        background=bg_color,
                        tabmargins=[2, 5, 2, 0]
                        )
        style.configure('TNotebook.Tab',
                        padding=[10, 5],
                        font=('Helvetica', 10)
                        )

        # Treeview (for lists)
        style.configure('Treeview',
                        font=('Helvetica', 10),
                        rowheight=25
                        )
        style.configure('Treeview.Heading',
                        font=('Helvetica', 10, 'bold'),
                        background=secondary_color,
                        foreground='white'
                        )

        # Entry fields
        style.configure('TEntry',
                        padding=5,
                        selectbackground=secondary_color
                        )

        # Return style object for further customization if needed
        return style

    def show_login_screen(self):
        """Show the login/register screen"""
        self._clear_frame()

        # Create centered container
        container = ttk.Frame(self.main_frame, style='Main.TFrame')
        container.grid(row=0, column=0, padx=20, pady=20)

        # Center the container
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        ttk.Label(
            container,
            text="Library Management System",
            style='Title.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Welcome message
        ttk.Label(
            container,
            text="Welcome! Please login or register to continue.",
            style='Subtitle.TLabel'
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Button frame
        button_frame = ttk.Frame(container, style='Main.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Login button
        login_btn = ttk.Button(
            button_frame,
            text="Login",
            command=self._show_login_dialog,
            style='Main.TButton',
            width=20
        )
        login_btn.grid(row=0, column=0, padx=10)

        # Register button
        register_btn = ttk.Button(
            button_frame,
            text="Register",
            command=self._show_register_dialog,
            style='Main.TButton',
            width=20
        )
        register_btn.grid(row=0, column=1, padx=10)

    def show_main_menu(self):
        """Central main menu with library functionality"""
        self._clear_frame()

        # Welcome header
        header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        header_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 20))
        ttk.Label(
            header_frame,
            text=f"Welcome, {self.current_user}!",
            style='Title.TLabel'
        ).pack(pady=10)

        # Create frames for different button categories
        book_management_frame = ttk.LabelFrame(self.main_frame, text="Book Management", style='Main.TFrame', padding=10)
        book_management_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

        user_actions_frame = ttk.LabelFrame(self.main_frame, text="User Actions", style='Main.TFrame', padding=10)
        user_actions_frame.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')

        features_frame = ttk.LabelFrame(self.main_frame, text="Features & Navigation", style='Main.TFrame', padding=10)
        features_frame.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        # Configure grid weights for frames
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Book Management buttons
        book_management_buttons = [
            ("Add Book", self._show_add_book_dialog),
            ("Remove Book", self._show_remove_book_dialog),
            ("Edit Book", self._show_edit_book_dialog),
            ("Book Features", self._show_book_features_dialog),
        ]

        # User Actions buttons
        user_actions_buttons = [
            ("Lend Book", self._show_lend_dialog),
            ("Return Book", self._show_return_dialog),
            ("Waiting Lists", self._show_waiting_list_dialog),
            ("Notifications", self._show_notifications),
        ]

        # Features & Navigation buttons
        features_buttons = [
            ("Search Book", self._show_search_dialog),
            ("View Book", self._show_view_books),
            ("Browse Books", self._show_book_navigation_dialog),
            ("Popular Books", self._show_popular_books),
        ]

        # Helper function to create buttons in a frame
        def create_buttons(frame, buttons):
            for i, (text, command) in enumerate(buttons):
                btn = ttk.Button(frame, text=text, command=command, style='Main.TButton')
                btn.pack(fill='x', pady=5, padx=5)

        # Create all buttons
        create_buttons(book_management_frame, book_management_buttons)
        create_buttons(user_actions_frame, user_actions_buttons)
        create_buttons(features_frame, features_buttons)

        # Logout button at the bottom
        logout_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        logout_frame.grid(row=2, column=0, columnspan=3, pady=20)
        ttk.Button(
            logout_frame,
            text="Logout",
            command=self._logout,
            style='Action.TButton'
        ).pack()

    def _show_login_dialog(self):
        """Show login dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Login")
        dialog.geometry("300x200")

        # Create a frame for the login form with padding
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(expand=True)

        # Username field
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, pady=5, padx=5, sticky='e')
        username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=username_var)
        username_entry.grid(row=0, column=1, pady=5, padx=5)

        # Password field
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, pady=5, padx=5, sticky='e')
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=5)

        def try_login():
            try:
                username = username_var.get()
                password = password_var.get()

                print(f"Attempting login for user: {username}")

                if self.user_manager.authenticate(username, password):
                    print("Authentication successful")
                    self.current_user = username
                    print(f"Registering {username} for notifications")
                    self.library.register_user_for_notifications(username)
                    dialog.destroy()
                    self.show_main_menu()
                    self.library._log_operation("logged in successfully")
                else:
                    print("Authentication failed")
                    self.library._log_operation("login failed", is_error=True)
                    messagebox.showerror("Error", "Invalid credentials")
            except Exception as e:
                print(f"Login error: {str(e)}")
                messagebox.showerror("Error", f"Login error: {str(e)}")

        # Login button
        login_button = ttk.Button(form_frame, text="Login", command=try_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Bind Enter key to log in
        dialog.bind('<Return>', lambda e: try_login())

        # Focus username field
        username_entry.focus()

        # Login button - Make sure this is properly placed
        login_button = ttk.Button(form_frame, text="Login", command=try_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Bind Enter key to log in
        dialog.bind('<Return>', lambda e: try_login())

        # Focus username field
        username_entry.focus()

    def _show_notifications(self):
        """Show user notifications"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Notifications")
        dialog.geometry("400x300")

        print(f"Checking notifications for {self.current_user}")
        print(f"Number of observers: {len(self.library.notification_center._observers)}")

        # Create treeview for notifications
        tree = ttk.Treeview(dialog, columns=("Time", "Message"))
        tree.heading("Time", text="Time")
        tree.heading("Message", text="Message")
        tree.column("#0", width=0, stretch=tk.NO)

        # Get all notifications for current user
        user_notifications = self.library.notification_center.get_user_notifications(self.current_user)
        print(f"Found {len(user_notifications)} notifications for {self.current_user}")

        if user_notifications:
            for notification in user_notifications:
                tree.insert("", "end", values=(
                    notification.timestamp.strftime("%Y-%m-%d %H:%M"),
                    notification.message
                ))
        else:
            ttk.Label(dialog, text="No notifications").pack(pady=20)

        tree.pack(fill='both', expand=True)

        # Clear button
        def clear_notifications():
            self.library.notification_center.clear_user_notifications(self.current_user)
            for item in tree.get_children():
                tree.delete(item)
            ttk.Label(dialog, text="No notifications").pack(pady=20)

        ttk.Button(
            dialog,
            text="Clear All",
            command=clear_notifications
        ).pack(pady=10)

    def _show_register_dialog(self):
        """Show registration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Register")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Username:").grid(row=0, column=0, pady=5, padx=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(dialog, textvariable=username_var)
        username_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(dialog, text="Password:").grid(row=1, column=0, pady=5, padx=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(dialog, textvariable=password_var, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=5)

        def try_register():
            username = username_var.get()
            password = password_var.get()

            if self.user_manager.register(username, password):
                dialog.destroy()
                messagebox.showinfo("Success", "Registration successful! Please login.")
                self.library._log_operation("registered successfully")
            else:
                messagebox.showerror("Error", "Username already exists")
                self.library._log_operation("registration failed", is_error=True)

        ttk.Button(dialog, text="Register", command=try_register).grid(row=2, column=0, columnspan=2, pady=10)

    def _show_add_book_dialog(self):
        """Show dialog for adding a book"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("400x300")

        # Create entry fields for book details
        fields = {}
        for i, field in enumerate(["title", "author", "copies", "genre", "year"]):
            ttk.Label(dialog, text=f"{field.title()}:").grid(row=i, column=0, pady=5, padx=5)
            var = tk.StringVar()
            fields[field] = var
            ttk.Entry(dialog, textvariable=var).grid(row=i, column=1, pady=5, padx=5)

        def try_add_book():
            try:
                copies = int(fields["copies"].get())
                year = int(fields["year"].get())

                success = self.library.add_book(
                    fields["title"].get(),
                    fields["author"].get(),
                    copies,
                    fields["genre"].get(),
                    year
                )

                if success:
                    dialog.destroy()
                    messagebox.showinfo("Success", "Book added successfully")
                else:
                    messagebox.showerror("Error", "Failed to add book")
            except ValueError:
                messagebox.showerror("Error", "Invalid number format")

        ttk.Button(dialog, text="Add Book", command=try_add_book).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def _show_remove_book_dialog(self):
        """Show dialog for removing a book from the library with consistent styling"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Book")

        # Center the dialog on the screen
        dialog_width = 400
        dialog_height = 200
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x_position = (screen_width - dialog_width) // 2
        y_position = (screen_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")

        # Add padding around the dialog
        dialog_frame = ttk.Frame(dialog, padding=(10, 10, 10, 10))
        dialog_frame.pack(fill="both", expand=True)

        # Label and entry for book title
        ttk.Label(dialog_frame, text="Book Title:", style="TLabel").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        title_var = tk.StringVar()
        ttk.Entry(dialog_frame, textvariable=title_var, style="TEntry", width=30).grid(row=0, column=1, pady=5, padx=5)

        def try_remove_book():
            title = title_var.get().strip()
            if not title:
                messagebox.showerror("Error", "Please enter a valid book title.")
                return

            # Attempt to remove the book
            success = self.library.remove_book(title)
            if success:
                dialog.destroy()
                messagebox.showinfo("Success", f"Book '{title}' removed successfully.")
            else:
                messagebox.showerror("Error",
                                     f"Failed to remove book '{title}'. Please check the logs for more details.")

        # Add a button to confirm removal
        ttk.Button(dialog_frame, text="Remove Book", command=try_remove_book, style="TButton").grid(
            row=1, column=0, columnspan=2, pady=10, sticky="ew"
        )

        # Add spacing between rows
        dialog_frame.grid_rowconfigure(0, weight=1)
        dialog_frame.grid_rowconfigure(1, weight=1)
        dialog_frame.grid_columnconfigure(1, weight=1)

    def _show_popular_books(self):
        """Show popular books based on waiting lists and borrow history"""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("Popular Books")
            dialog.geometry("800x500")

            # Create notebook for different popularity metrics
            notebook = ttk.Notebook(dialog)
            notebook.pack(fill='both', expand=True)

            # Create frames for different metrics
            waiting_frame = ttk.Frame(notebook)
            borrowed_frame = ttk.Frame(notebook)
            notebook.add(waiting_frame, text="Most Wanted")
            notebook.add(borrowed_frame, text="Most Borrowed")

            # Function to create trees
            def create_tree(parent, extra_column):
                tree = ttk.Treeview(parent, columns=("Title", "Author", "Genre", extra_column))
                tree.heading("Title", text="Title")
                tree.heading("Author", text="Author")
                tree.heading("Genre", text="Genre")
                tree.heading(extra_column, text=extra_column)
                tree.column("#0", width=0, stretch=tk.NO)

                # Add scrollbar
                scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                return tree

            # Create and populate "Most Wanted" tree
            waiting_tree = create_tree(waiting_frame, "Waiting List")
            waiting_books = [(book, len(self.library.get_waiting_list(book.title)))
                             for book in self.library.get_all_books()]
            waiting_books.sort(key=lambda x: x[1], reverse=True)  # Sort by waiting list size

            for book, waiting_count in waiting_books:
                if waiting_count > 0:  # Only show books with people waiting
                    waiting_tree.insert("", "end", values=(
                        book.title,
                        book.author,
                        book.genre,
                        waiting_count
                    ))

            borrowed_tree = create_tree(borrowed_frame, "Times Borrowed")
            borrowed_books = [(book, book.total_borrows)
                              for book in self.library.get_all_books()]
            borrowed_books.sort(key=lambda x: x[1], reverse=True)  # Sort by borrow count

            # Show top 10 most borrowed books or all if less than 10
            for book, borrow_count in borrowed_books[:10]:
                if borrow_count > 0:  # Only show books that have been borrowed
                    borrowed_tree.insert("", "end", values=(
                        book.title,
                        book.author,
                        book.genre,
                        borrow_count
                    ))

            self.library._log_operation("Displayed popular books successfully")
        except Exception as e:
            self.library._log_operation("Failed to display popular books", is_error=True)
            messagebox.showerror("Error", f"Error displaying popular books: {str(e)}")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

    def _show_search_dialog(self):
        """Show dialog for searching books"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Books")
        dialog.geometry("400x500")

        # Search criteria
        ttk.Label(dialog, text="Search by:").grid(row=0, column=0, pady=5, padx=5)
        strategy_var = tk.StringVar(value="title")
        strategies = ["title", "author", "genre", "year"]
        strategy_menu = ttk.OptionMenu(dialog, strategy_var, "title", *strategies)
        strategy_menu.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(dialog, text="Search query:").grid(row=1, column=0, pady=5, padx=5)
        query_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=query_var).grid(row=1, column=1, pady=5, padx=5)

        # Results list
        results_frame = ttk.Frame(dialog)
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        results_list = ttk.Treeview(results_frame, columns=("Title", "Author", "Genre", "Available"))
        results_list.heading("Title", text="Title")
        results_list.heading("Author", text="Author")
        results_list.heading("Genre", text="Genre")
        results_list.heading("Available", text="Available")
        results_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        def perform_search():
            results_list.delete(*results_list.get_children())
            try:
                books = self.library.search_books(strategy_var.get(), query_var.get())
                for book in books:
                    results_list.insert("", "end", values=(
                        book.title,
                        book.author,
                        book.genre,
                        "Yes" if book.is_available else "No"
                    ))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Search", command=perform_search).grid(row=3, column=0, columnspan=2, pady=10)

    def _show_view_books(self):
        """Show all books in the library"""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("View Books")
            dialog.geometry("600x400")

            # Create notebook for different views
            notebook = ttk.Notebook(dialog)
            notebook.pack(fill='both', expand=True)

            # Create tabs for different views
            all_frame = ttk.Frame(notebook)
            available_frame = ttk.Frame(notebook)
            borrowed_frame = ttk.Frame(notebook)
            category_frame = ttk.Frame(notebook)

            notebook.add(all_frame, text="All Books")
            notebook.add(available_frame, text="Available Books")
            notebook.add(borrowed_frame, text="Borrowed Books")
            notebook.add(category_frame, text="By Category")

            # Populate all books
            try:
                self._populate_book_list(all_frame, self.library.get_all_books())
                self.library._log_operation("Displayed all books successfully")
            except Exception as e:
                self.library._log_operation("Failed to display all books", is_error=True)
                raise

            # Populate available books
            try:
                self._populate_book_list(available_frame, self.library.get_available_books())
                self.library._log_operation("Displayed available books successfully")
            except Exception as e:
                self.library._log_operation("Failed to display available books", is_error=True)
                raise

            # Populate borrowed books
            try:
                self._populate_book_list(borrowed_frame, self.library.get_loaned_books())
                self.library._log_operation("Displayed borrowed books successfully")
            except Exception as e:
                self.library._log_operation("Failed to display borrowed books", is_error=True)
                raise

            # Add category selection
            try:
                categories = sorted(set(book.genre for book in self.library.get_all_books()))
                category_var = tk.StringVar()
                category_selector = ttk.Combobox(category_frame, textvariable=category_var, values=categories)
                category_selector.pack(pady=5)

                def show_category():
                    category = category_var.get()
                    books = [book for book in self.library.get_all_books() if book.genre == category]
                    self._populate_book_list(category_frame, books)
                    self.library._log_operation(f"Displayed books by category '{category}' successfully")

                ttk.Button(category_frame, text="Show Category", command=show_category).pack(pady=5)
            except Exception as e:
                self.library._log_operation("Failed to display books by category", is_error=True)
                raise

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying books: {str(e)}")

    def _show_lend_dialog(self):
        """Show dialog for lending a book"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Lend Book")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Book Title:").grid(row=0, column=0, pady=5, padx=5)
        title_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=title_var).grid(row=0, column=1, pady=5, padx=5)

        def try_lend_book():
            title = title_var.get()
            if self.library.loan_book(title, self.current_user):
                dialog.destroy()
                messagebox.showinfo("Success", "Book borrowed successfully")
            else:
                messagebox.showerror("Error", "Failed to borrow book")

        ttk.Button(dialog, text="Borrow", command=try_lend_book).grid(row=1, column=0, columnspan=2, pady=10)

    def _show_edit_book_dialog(self):
        """Show dialog for editing book details"""
        # First, show a dialog to select the book to edit
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book - Select Book")
        dialog.geometry("400x150")

        ttk.Label(dialog, text="Enter Book Title:").grid(row=0, column=0, pady=5, padx=5)
        title_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=title_var).grid(row=0, column=1, pady=5, padx=5)

        def show_edit_fields():
            title = title_var.get()
            book = self.library._get_book_case_insensitive(title)
            if not book:
                messagebox.showerror("Error", "Book not found")
                return

            # Close selection dialog
            dialog.destroy()

            # Create edit dialog
            edit_dialog = tk.Toplevel(self.root)
            edit_dialog.title("Edit Book Details")
            edit_dialog.geometry("400x300")

            # Create variables for each field
            fields = {
                'title': tk.StringVar(value=book.title),
                'author': tk.StringVar(value=book.author),
                'genre': tk.StringVar(value=book.genre),
                'year': tk.StringVar(value=str(book.year)),
                'copies': tk.StringVar(value=str(book.copies))
            }

            # Create entry fields
            for i, (field, var) in enumerate(fields.items()):
                ttk.Label(edit_dialog, text=f"{field.title()}:").grid(row=i, column=0, pady=5, padx=5)
                ttk.Entry(edit_dialog, textvariable=var).grid(row=i, column=1, pady=5, padx=5)

            def save_changes():
                try:
                    updates = {
                        'title': fields['title'].get(),
                        'author': fields['author'].get(),
                        'genre': fields['genre'].get(),
                        'year': int(fields['year'].get()),
                        'copies': int(fields['copies'].get())
                    }

                    if self.library.update_book(book.title, updates):
                        edit_dialog.destroy()
                        messagebox.showinfo("Success", "Book updated successfully")
                    else:
                        messagebox.showerror("Error", "Failed to update book")

                except ValueError:
                    messagebox.showerror("Error", "Invalid number format for year or copies")

            ttk.Button(edit_dialog, text="Save Changes", command=save_changes).grid(row=len(fields), column=0,
                                                                                    columnspan=2, pady=10)

        ttk.Button(dialog, text="Edit Book", command=show_edit_fields).grid(row=1, column=0, columnspan=2, pady=10)

    def _show_return_dialog(self):
        """Show dialog for returning a book"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Return Book")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Book Title:").grid(row=0, column=0, pady=5, padx=5)
        title_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=title_var).grid(row=0, column=1, pady=5, padx=5)

        def try_return_book():
            title = title_var.get()
            if self.library.return_book(title, self.current_user):
                dialog.destroy()
                messagebox.showinfo("Success", "Book returned successfully")
            else:
                messagebox.showerror("Error", "Failed to return book")

        ttk.Button(dialog, text="Return Book", command=try_return_book).grid(row=1, column=0, columnspan=2, pady=10)

    @staticmethod
    def _populate_book_list(parent: ttk.Frame, books: List[Book]):
        """Helper method to populate a book list in a frame"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        # Create and set up treeview
        tree = ttk.Treeview(parent, columns=("Title", "Author", "Genre", "Copies", "Available"))
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Genre", text="Genre")
        tree.heading("Copies", text="Total Copies")
        tree.heading("Available", text="Available Copies")
        tree.column("#0", width=0, stretch=tk.NO)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Populate data
        for book in books:
            tree.insert("", "end", values=(
                book.title,
                book.author,
                book.genre,
                book.copies,
                book.available_copies
            ))

        # Pack widgets
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_book_features_dialog(self):
        """Show dialog for managing book features"""
        # First, select a book
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Book Features")
        dialog.geometry("500x500")  # Made taller to accommodate buttons

        ttk.Label(dialog, text="Select Book:").grid(row=0, column=0, pady=5, padx=5)
        book_var = tk.StringVar()
        book_select = ttk.Combobox(dialog, textvariable=book_var)
        book_select['values'] = [book.title for book in self.library.get_all_books()]
        book_select.grid(row=0, column=1, pady=5, padx=5)

        # Feature selection frame
        features_frame = ttk.LabelFrame(dialog, text="Add Features")
        features_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        # Digital Version
        digital_var = tk.BooleanVar()
        digital_check = ttk.Checkbutton(features_frame, text="Digital Version", variable=digital_var)
        digital_check.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        # Audiobook
        audio_var = tk.BooleanVar()
        audio_check = ttk.Checkbutton(features_frame, text="Audiobook", variable=audio_var)
        audio_check.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        # Award Winner
        award_var = tk.BooleanVar()
        award_check = ttk.Checkbutton(features_frame, text="Award Winner", variable=award_var)
        award_check.grid(row=2, column=0, pady=5, padx=5, sticky="w")

        # Preview frame
        preview_frame = ttk.LabelFrame(dialog, text="Preview")
        preview_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")

        preview_text = tk.Text(preview_frame, height=8, width=50)
        preview_text.pack(padx=5, pady=5, fill="both", expand=True)

        def update_preview():
            """Update the preview text with current features"""
            title = book_var.get()
            if not title:
                return

            book = self.library._get_book_case_insensitive(title)
            if not book:
                return

            # Load existing features if any
            # current_features = self.library.get_book_features(title)

            # Start with base book description
            preview_text.delete(1.0, tk.END)
            preview_text.insert(tk.END, f"Title: {book.title}\n")
            preview_text.insert(tk.END, f"Author: {book.author}\n")
            preview_text.insert(tk.END, f"Genre: {book.genre}\n")
            preview_text.insert(tk.END, f"Year: {book.year}\n\n")

            # Add current and selected features
            preview_text.insert(tk.END, "Features:\n")
            if digital_var.get():
                preview_text.insert(tk.END, "- Digital Version Available\n")
            if audio_var.get():
                preview_text.insert(tk.END, "- Audiobook Available\n")
            if award_var.get():
                preview_text.insert(tk.END, "- Award Winner\n")

        def save_features():
            """Save the selected features"""
            title = book_var.get()
            if not title:
                messagebox.showwarning("Warning", "Please select a book first")
                return

            features = []
            if digital_var.get():
                features.append("Digital Version")
            if audio_var.get():
                features.append("Audiobook")
            if award_var.get():
                features.append("Award Winner")

            success = self.library.update_book_features(title, features)
            if success:
                messagebox.showinfo("Success", "Features saved successfully!")
                update_preview()
            else:
                messagebox.showerror("Error", "Failed to save features")

        # Add buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Add preview and save buttons
        ttk.Button(buttons_frame, text="Preview", command=update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Features", command=save_features).pack(side=tk.LEFT, padx=5)

        # Initial preview
        book_select.bind('<<ComboboxSelected>>', lambda e: update_preview())

    def _logout(self):
        """Handle user logout"""
        self.current_user = None
        self.library._log_operation("log out successful")
        self.show_login_screen()

    def _show_waiting_list_dialog(self):
        """Show dialog for managing waiting lists"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Waiting Lists")
        dialog.geometry("600x500")

        # Create notebook for different views
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # My Waiting Lists tab
        my_lists_frame = ttk.Frame(notebook)
        available_books_frame = ttk.Frame(notebook)

        notebook.add(my_lists_frame, text="My Waiting Lists")
        notebook.add(available_books_frame, text="Join Waiting List")

        # === My Waiting Lists Tab ===
        my_tree = ttk.Treeview(my_lists_frame, columns=("Title", "Author", "Position"))
        my_tree.heading("Title", text="Title")
        my_tree.heading("Author", text="Author")
        my_tree.heading("Position", text="Position in Line")
        my_tree.column("#0", width=0, stretch=tk.NO)

        # Add scrollbar
        my_scrollbar = ttk.Scrollbar(my_lists_frame, orient="vertical", command=my_tree.yview)
        my_tree.configure(yscrollcommand=my_scrollbar.set)

        my_tree.pack(side="left", fill="both", expand=True)
        my_scrollbar.pack(side="right", fill="y")

        def update_my_lists():
            my_tree.delete(*my_tree.get_children())
            positions = self.library.get_user_waiting_list_positions(self.current_user)

            for title, position in positions.items():
                book = self.library._get_book_case_insensitive(title)
                if book:
                    my_tree.insert("", "end", values=(
                        book.title,
                        book.author,
                        f"{position} of {len(self.library.get_waiting_list(title))}"
                    ))

        def leave_waiting_list():
            selection = my_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a book to leave its waiting list")
                return

            item = my_tree.item(selection[0])
            title = item['values'][0]

            if self.library.remove_from_waiting_list(title, self.current_user):
                self.library.unregister_user_from_notifications(self.current_user)
                messagebox.showinfo("Success", f"Removed from waiting list for '{title}'")
                update_my_lists()
            else:
                messagebox.showerror("Error", "Failed to leave waiting list")

        ttk.Button(my_lists_frame, text="Leave Selected List", command=leave_waiting_list).pack(pady=5)

        # === Join Waiting List Tab ===
        available_tree = ttk.Treeview(available_books_frame, columns=("Title", "Author", "Genre", "Waiting"))
        available_tree.heading("Title", text="Title")
        available_tree.heading("Author", text="Author")
        available_tree.heading("Genre", text="Genre")
        available_tree.heading("Waiting", text="People Waiting")
        available_tree.column("#0", width=0, stretch=tk.NO)

        # Add scrollbar
        available_scrollbar = ttk.Scrollbar(available_books_frame, orient="vertical", command=available_tree.yview)
        available_tree.configure(yscrollcommand=available_scrollbar.set)

        available_tree.pack(side="left", fill="both", expand=True)
        available_scrollbar.pack(side="right", fill="y")

        def update_available_books():
            available_tree.delete(*available_tree.get_children())
            for book in self.library.get_all_books():
                if not book.is_available:
                    waiting_list = self.library.get_waiting_list(book.title)
                    available_tree.insert("", "end", values=(
                        book.title,
                        book.author,
                        book.genre,
                        len(waiting_list)
                    ))

        def join_waiting_list():
            selection = available_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a book to join its waiting list")
                return

            item = available_tree.item(selection[0])
            title = item['values'][0]

            if self.library.add_to_waiting_list(title, self.current_user):
                messagebox.showinfo("Success", f"Added to waiting list for '{title}'")
                update_my_lists()
                update_available_books()
            else:
                messagebox.showerror("Error", "Failed to join waiting list")

        ttk.Button(available_books_frame, text="Join Selected List", command=join_waiting_list).pack(pady=5)

        # Initial updates
        update_my_lists()
        update_available_books()

        # Refresh button
        ttk.Button(dialog, text="Refresh Lists",
                   command=lambda: [update_my_lists(), update_available_books()]).pack(pady=5)

    def _show_book_navigation_dialog(self):
        """Show dialog for navigating books using different iterators."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Browse Books")
        dialog.geometry("600x500")

        # Create frames
        control_frame = ttk.Frame(dialog)
        control_frame.pack(fill='x', padx=5, pady=5)

        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Iterator selection
        ttk.Label(control_frame, text="Browse by:").grid(row=0, column=0, padx=5)
        iterator_var = tk.StringVar(value="chronological")
        iterator_options = {
            "chronological": "Year",
            "alphabetical": "Alphabetical",
            "genre": "Genre",
            "popularity": "Popularity",
            "availability": "Availability"
        }
        iterator_menu = ttk.OptionMenu(
            control_frame,
            iterator_var,
            "chronological",
            *iterator_options.keys()
        )
        iterator_menu.grid(row=0, column=1, padx=5)

        # Additional options frame
        options_frame = ttk.LabelFrame(control_frame, text="Options")
        options_frame.grid(row=0, column=2, padx=5)

        reverse_var = tk.BooleanVar()
        by_author_var = tk.BooleanVar()
        available_only_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Reverse Order", variable=reverse_var).pack(padx=5)
        ttk.Checkbutton(options_frame, text="By Author", variable=by_author_var).pack(padx=5)
        ttk.Checkbutton(options_frame, text="Available Only", variable=available_only_var).pack(padx=5)

        # Create treeview for books
        tree = ttk.Treeview(list_frame, columns=("Title", "Author", "Year", "Genre", "Status"))
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Year", text="Year")
        tree.heading("Genre", text="Genre")
        tree.heading("Status", text="Status")
        tree.column("#0", width=0, stretch=tk.NO)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def update_list():
            # Clear current items
            for item in tree.get_children():
                tree.delete(item)

            # Get selected iterator type
            iterator_type = iterator_var.get()

            try:
                # Configure iterator using LibrarySystem
                kwargs = {
                    'reverse': reverse_var.get(),
                    'by_author': by_author_var.get(),
                    'available_only': available_only_var.get()
                }
                iterator = self.library.get_iterator(iterator_type, **kwargs)

                # Add items
                current_group = None
                for book in iterator:
                    if iterator_type == 'genre' and isinstance(iterator, GenreIterator):
                        new_group = iterator.current_genre()
                        if new_group != current_group:
                            current_group = new_group
                            tree.insert("", "end", values=("", f"== {current_group} ==", "", "", ""))

                    tree.insert("", "end", values=(
                        book.title,
                        book.author,
                        book.year,
                        book.genre,
                        "Available" if book.is_available else "Unavailable"
                    ))

                self.library._log_operation(
                    f"Book navigation using {iterator_options[iterator_type]} view completed successfully")
            except Exception as e:
                self.library._log_operation(f"Book navigation failed: {str(e)}", is_error=True)
                messagebox.showerror("Error", f"Failed to load books: {str(e)}")

        # Add refresh button
        ttk.Button(control_frame, text="Refresh", command=update_list).grid(row=0, column=3, padx=5)

        # Initial load
        update_list()


if __name__ == "__main__":
    app = LibraryGUI()
    app.run()
    var = tk.StringVar()
    ttk.Entry(dialog, textvariable=title_var).grid(row=0, column=1, pady=5, padx=5)
