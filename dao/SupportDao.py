import sqlite3
from datetime import datetime


class SupportDao:
    def __init__(self, conn):
        self.conn = conn

    def get_tickets_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
           SELECT s.SupportMessageID, s.Subject, s.MessageText, MAX(s.MessageDate) AS LastModified, s.Status, u.username AS Username 
            FROM SupportMessages s
            JOIN users u ON u.userid = s.userid
            Where s.userid = ?
            GROUP BY SupportMessageID
            ORDER BY LastModified DESC
        """, (user_id,))
        tickets = cursor.fetchall()
        cursor.close()
        return tickets

    def get_all_tickets(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.SupportMessageID, s.Subject, s.MessageText, MAX(s.MessageDate) AS LastModified, s.Status, u.username AS Username 
            FROM SupportMessages s
            JOIN users u ON u.userid = s.userid
            GROUP BY SupportMessageID
            ORDER BY LastModified DESC
        """)
        tickets = cursor.fetchall()
        cursor.close()
        return tickets

    def get_ticket_by_id(self, support_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.SupportMessageID, s.Subject, s.MessageText, s.MessageDate, s.Status, u.username, LibrarianID
            FROM SupportMessages s
            JOIN users u ON u.userid = s.userid
            WHERE SupportMessageID = ?
        """, (support_id,))
        ticket = cursor.fetchone()
        cursor.close()
        return ticket

    def update_ticket_status(self, support_id, status):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE SupportMessages
                SET Status = ?
                WHERE SupportMessageID = ?
            """, (status, support_id))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error updating ticket status: {e}")

    def create_support_message(self, user_id, subject, message_text):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO SupportMessages (UserID, Subject, MessageText, MessageDate)
                VALUES (?, ?, ?, ?)
            """, (user_id, subject, message_text, datetime.now()))
            self.conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Error creating support message: {e}")

    def get_support_comments(self, support_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sc.CommentText, sc.CommentDate, u.UserName, u.Role
            FROM SupportComments sc
            JOIN Users u ON sc.UserID = u.UserID
            WHERE sc.SupportMessageID = ?
            ORDER BY sc.CommentDate DESC
        """, (support_id,))
        comments = cursor.fetchall()
        cursor.close()
        return comments

    def add_support_comment(self, support_id, user_id, comment_text):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO SupportComments (SupportMessageID, UserID, CommentText, CommentDate)
                VALUES (?, ?, ?, ?)
            """, (support_id, user_id, comment_text, datetime.now()))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error adding support comment: {e}")

    def close_connection(self):
        self.conn.close()
