import sqlite3

from bean.WishList import Wishlist


class WishlistDao:
    def __init__(self, conn):
        self.conn = conn

    def book_in_wishlist(self, user_id, title, author, genre):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM Wishlist 
                WHERE UserID = ? AND BookTitle = ? AND BookAuthor = ? AND Genre = ?
            """, (user_id, title, author, genre))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except sqlite3.Error as e:
            print(f"Error checking book in wishlist: {e}")
            return False

    def add_book_to_wishlist(self, user_id, title, author, genre):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Wishlist (UserID, BookTitle, BookAuthor, Genre, IsAvailable)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, title, author, genre, 0))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error adding book to wishlist: {e}")

    def get_wishlist_by_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT WishlistID, BookTitle, BookAuthor, Genre, IsAvailable
                FROM Wishlist
                WHERE UserID = ?
            """, (user_id,))
            rows = cursor.fetchall()
            cursor.close()
            wishlist = [Wishlist(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            return wishlist
        except sqlite3.Error as e:
            print(f"Error fetching wishlist: {e}")
            return []

    def remove_book_from_wishlist(self, wishlist_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM Wishlist
                WHERE WishlistID = ?
            """, (wishlist_id,))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error removing book from wishlist: {e}")

    def update_book_availability(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Wishlist
                SET IsAvailable = 1
                WHERE BookTitle IN (
                    SELECT BookTitle
                    FROM Books
                )
            """)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error updating book availability in wishlist: {e}")