import sqlite3
from datetime import datetime


class ActivityDao:
    def __init__(self, conn):
        self.conn = conn

    def log_activity(self, user_id, activity_type):
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO History (UserID, Action, ActionDate) VALUES (?, ?, ?)"
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (user_id, activity_type, date))
            self.conn.commit()
            cursor.close()
            print("User activity logged successfully")
        except sqlite3.Error as err:
            print(f"Error logging user activity: {err}")

    def log_activity_support(self, user_id, activity_type, SupportMessageID):
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO History (UserID, Action, ActionDate, SupportMessageID) VALUES (?, ?, ?,?)"
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (user_id, activity_type, date, SupportMessageID))
            self.conn.commit()
            cursor.close()
            print("Support Message activity logged successfully")
        except sqlite3.Error as err:
            print(f"Error logging user activity: {err}")

    def log_activity_book(self, user_id, activity_type, bookid):
        print(f"Logging activity: UserID={user_id}, Action={activity_type}, BookID={bookid}")
        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO History (UserID, Action, ActionDate, BookID) VALUES (?, ?, ?, ?)"
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Executing query: {insert_query} with values ({user_id}, {activity_type}, {date}, {bookid})")
            cursor.execute(insert_query, (user_id, activity_type, date, bookid))
            self.conn.commit()
            cursor.close()
            print("Book activity logged successfully")
        except sqlite3.Error as err:
            print(f"Error logging user activity: {err}")
