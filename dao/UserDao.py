import sqlite3

from bean.History import History
from bean.User import User


class UserDao:
    def __init__(self, conn):
        self.conn = conn

    def authenticate_user(self, username, password):
        try:
            query = """
            SELECT UserID, UserName, Password, UserEmail, UserPhone, Role
            FROM users
            WHERE UserName = ? AND Password = ?
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return User(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def get_all_users(self):
        try:
            query = """
            SELECT UserID, UserName, UserEmail, UserPhone, Role
            FROM Users
            """
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            users = []
            for result in results:
                users.append(User(result[0], result[1], None, result[2], result[3], result[4]))
            return users
        except sqlite3.Error as e:
            print(f"Error fetching all users: {e}")
            return []

    def get_user_by_username(self, username):
        try:
            query = """
                SELECT UserID, UserName, Password, UserEmail, UserPhone, Role
                FROM users
                WHERE UserName = ?
                """
            cursor = self.conn.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return User(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def get_user_by_id(self, username):
        try:
            query = """
                SELECT UserID, UserName, Password, UserEmail, UserPhone, Role
                FROM users
                WHERE userid = ?
                """
            cursor = self.conn.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return User(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def create_user(self, username, email, phone, password, role):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Users (UserName, UserEmail, UserPhone, Password, Role) VALUES (?, ?, ?, ?, ?)",
                (username, email, phone, password, role)
            )
            self.conn.commit()  # Commit the transaction
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return False

    def change_password(self, user_id, new_password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Users
                SET Password = ?
                WHERE UserID = ?
            """, (new_password, user_id))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error changing password: {e}")

    def delete_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM Users
                WHERE UserID = ?
            """, (user_id,))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")

    def forgot_password(self, username, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ? AND useremail = ?", (username, email))
        return cursor.fetchone()