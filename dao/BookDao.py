import sqlite3

from sqlalchemy.engine import cursor

from bean.Book import Book
from model.merchantAPI import api_query


class BookDao:
    def __init__(self, conn):
        self.conn = conn

    def add_book(self, title, author, genre, branch_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Books (BookTitle, BookAuthor, Genre, BranchID) VALUES (?, ?, ?, ?)",
                       (title, author, genre, branch_id))
        self.conn.commit()

    def get_all_books(self):
        try:
            query = """
            SELECT *
            FROM Books
            """
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            books = []
            for result in results:
                books.append(Book(result[0], result[1], result[2], result[3], result[4], result[5]))
            return books
        except sqlite3.Error as e:
            print(f"Error fetching all users: {e}")
            return []

    def get_book_by_id(self, book_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
            result = cursor.fetchone()
            if result:
                book = Book(result[0], result[1], result[2], result[3], result[4], result[5])
                return book
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching book by ID: {e}")
            return None
    def get_book_by_title(self, book_title):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Books WHERE BookTitle = ?", (book_title,))
            result = cursor.fetchone()
            if result:
                book = Book(result[0], result[1], result[2], result[3], result[4], result[5])
                return book
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching book by ID: {e}")
            return None

    def add_rating(self, user_id, book_id, rating, review):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Ratings (UserID, BookID, Rating, Review) VALUES (?, ?, ?, ?)",
            (user_id, book_id, rating, review)
        )
        self.conn.commit()

    def get_ratings_by_book(self, book_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT r.UserID, u.UserName, r.Rating, r.Review "
                "FROM Ratings r "
                "INNER JOIN users u ON r.UserID = u.UserID "
                "WHERE r.BookID = ?",
                (book_id,)
            )
            ratings = cursor.fetchall()
            cursor.close()
            return ratings
        except sqlite3.Error as e:
            print(f"Error retrieving ratings for book {book_id}: {e}")
            return []

    def checkout_book(self, book_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT IsAvailable FROM Books WHERE BookID = ?", (book_id,))
        available = cursor.fetchone()[0]

        if not available:
            return False  # Book is already checked out

        cursor.execute("UPDATE Books SET IsAvailable = 0 WHERE BookID = ?", (book_id,))
        self.conn.commit()
        return True

    def return_book(self, book_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT UserID FROM History
            WHERE BookID = ? AND Action = 'Book Checkout'
            ORDER BY ActionDate DESC
            LIMIT 1
        """, (book_id,))
        last_user = cursor.fetchone()[0]
        print(last_user)
        if last_user != user_id:
            return False  # This user didn't check out the book
        cursor.execute("UPDATE Books SET IsAvailable = 1 WHERE BookID = ?", (book_id,))
        self.conn.commit()
        return True

    def get_books_not_in_library(self, search_query=None):
        try:
            # Fetch existing book titles from the database
            query = "SELECT BookTitle FROM Books"
            cursor = self.conn.cursor()
            cursor.execute(query)
            existing_book_titles = [result[0].lower() for result in cursor.fetchall()]
            cursor.close()

            # Fetch all books from the API
            all_books = api_query(search_query)  # Pass search_query to the API function

            # Filter books not in the database
            books_not_in_db = [book for book in all_books
                               if book.get_book_name().lower() not in existing_book_titles]

            return books_not_in_db

        except Exception as e:
            print(f"Error: {e}")
            return []

    def search_books(self, search_query):
        try:
            query = """
             SELECT *
             FROM Books
             WHERE BookTitle LIKE ? OR BookAuthor LIKE ? OR Genre LIKE ?
             """
            cursor = self.conn.cursor()
            like_query = f'%{search_query}%'
            cursor.execute(query, (like_query, like_query, like_query))
            results = cursor.fetchall()
            cursor.close()
            books = []
            for result in results:
                books.append(Book(result[0], result[1], result[2], result[3], result[4], result[5]))
            return books
        except sqlite3.Error as e:
            print(f"Error searching books: {e}")
            return []