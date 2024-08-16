import os
import random
import sqlite3


from flask import g, render_template
from model.merchantAPI import api_query, api_query_startup

DATABASE = 'library.db'

# Script meant to populate data on initial install
class DB_init:
    def __init__(self, app):
        self.app = app
    # init connection
    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    # load schema file in root of project
    def init_db(self):
        if not os.path.exists(DATABASE):
            with self.app.app_context():
                db = self.get_db()
                with self.app.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()
    # load fake data
    def insert_data(self):
        with self.app.app_context():
            db = self.get_db()
            if self.tables_empty(db):
                # Initialize data only if tables are empty
                users_data = [
                    ("user1", "john@example.com", "123-456-7890", "1", "customer"),
                    ("user2", "alice@example.com", "987-654-3210", "1", "librarian"),
                    ("user3", "alice2@example.com", "987-654-3210", "1", "customer")
                ]
                for user in users_data:
                    db.execute(
                        "INSERT INTO Users (UserName, UserEmail, UserPhone, Password, Role) VALUES (?, ?, ?, ?, ?)",
                        user)

                branches_data = [
                    ("Main Library", "City Center"),
                    ("Kiosk Library", "Mail")
                ]
                for branch in branches_data:
                    db.execute("INSERT INTO Branches (BranchName, BranchLocation) VALUES (?, ?)", branch)

                books_data = api_query_startup()

                for book in books_data:
                    random_value = random.choice([1, 2])
                    db.execute(
                                "INSERT INTO Books (BookTitle, BookAuthor, Genre, BranchID, IsAvailable) VALUES (?, ?, ?, ?, 1)",
        (book.get_book_name(), book.get_book_author(), book.get_genre(), random_value)
    )

                history_data = [
                    (1, 1, 'Book Checkout', '2024-05-21'),
                    (2, 3, 'Book Checkout', '2024-05-21')

                ]
                for history in history_data:
                    db.execute("INSERT INTO History (BookID, UserID, Action, ActionDate) VALUES (?, ?, ?, ?)", history)

                ratings_data = [
                    (1, 1, 1, 5, "Great book"),
                    (2, 2, 2, 4, "Interesting read")
                ]
                for rating in ratings_data:
                    db.execute("INSERT INTO Ratings (RatingID, UserID, BookID, Rating, Review) VALUES (?, ?, ?, ?, ?)",
                               rating)

                support_messages_data = [
                    (1, None, "Need Help", "Hey help me find a new book called, new book", '2024-05-21', 'open'),
                    (2, 1, "Website Issue", "When i try to add to my wishlist it is slow", '2024-05-22', 'open')
                ]
                for message in support_messages_data:
                    db.execute("INSERT INTO SupportMessages (UserID, LibrarianID, Subject,"
                               " MessageText, MessageDate, Status) VALUES (?, ?, ?, ?, ?, ?)", message)

                db.commit()
         # Simple Count check for if tables are empty using count
    def tables_empty(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Branches")
        branch_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Books")
        book_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM History")
        history_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Wishlist")
        wishlist_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Ratings")
        ratings_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM SupportMessages")
        support_messages_count = cursor.fetchone()[0]
        return (user_count == 0 and branch_count == 0 and book_count == 0 and history_count == 0
                and wishlist_count == 0 and ratings_count == 0 and
                support_messages_count == 0)


