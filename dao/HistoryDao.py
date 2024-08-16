import sqlite3
from bean.History import History

class HistoryDao:
    def __init__(self, conn):
        self.conn = conn

    def get_history_by_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                 SELECT h.HistoryID, h.BookID, h.UserID, h.Action, h.ActionDate, h.SupportMessageID, u.UserName
                 FROM History h
                 JOIN Users u ON h.UserID = u.UserID
                 WHERE h.UserID = ?
                 ORDER BY h.ActionDate DESC
             """, (user_id,))
            rows = cursor.fetchall()
            cursor.close()

            history_entries = []
            for row in rows:
                history_entry = History(
                    row[0],  # history_id
                    row[1],  # book_id
                    row[2],  # user_id
                    row[3],  # action
                    row[4],  # action_date
                    row[5]  # support_message_id
                )
                history_entries.append(history_entry)

            return history_entries

        except sqlite3.Error as e:
            print(f"Error fetching history: {e}")
            return []

    def get_late_books(self):
        try:
            query = """
            SELECT 
                h.BookID, 
                b.BookTitle, 
                b.BookAuthor, 
                b.Genre, 
                h.UserID, 
                u.username,
                julianday('now') - julianday(
                    CASE 
                        WHEN instr(h.ActionDate, ' ') > 0 THEN h.ActionDate
                        ELSE h.ActionDate || ' 00:00:00'
                    END
                ) AS DaysLate
            FROM 
                History h
            JOIN 
                Books b ON h.BookID = b.BookID
            JOIN 
                 Users u ON h.UserID = u.UserID
            WHERE 
                h.Action = 'Book Checkout' AND 
                (julianday('now') - julianday(
                    CASE 
                        WHEN instr(h.ActionDate, ' ') > 1 THEN h.ActionDate
                        ELSE h.ActionDate || ' 00:00:00'
                    END
                )) > 3 AND 
                NOT EXISTS (
                    SELECT 1
                    FROM History h2
                    WHERE h2.BookID = h.BookID 
                      AND h2.UserID = h.UserID 
                      AND h2.Action = 'Book Returned' 
                      AND julianday(h2.ActionDate) > julianday(h.ActionDate)
                )
            """
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Print out the raw results for debugging
            print("Raw Results from Query:")
            for row in results:
                print(row)

            late_books = []
            for result in results:
                late_books.append({
                    'book_id': result[0],
                    'title': result[1],
                    'author': result[2],
                    'genre': result[3],
                    'user_id': result[4],
                    'username': result[5],
                    'days_late': int(result[6])
                })

            # Print out the processed late_books list for debugging
            print("Processed Late Books List:")
            for book in late_books:
                print(book)

            return late_books

        except sqlite3.Error as e:
            print(f"Error fetching late books: {e}")
            return []

    def get_late_books_by_user(self, user_id):
        try:
            query = """
            SELECT 
                h.BookID, 
                b.BookTitle, 
                b.BookAuthor, 
                b.Genre, 
                h.UserID, 
                u.username,
                julianday('now') - julianday(
                    CASE 
                        WHEN instr(h.ActionDate, ' ') > 0 THEN h.ActionDate
                        ELSE h.ActionDate || ' 00:00:00'
                    END
                ) AS DaysLate
            FROM 
                History h
            JOIN 
                Books b ON h.BookID = b.BookID
            JOIN 
                Users u ON h.UserID = u.UserID
            WHERE
                u.UserID = ? AND 
                h.Action = 'Book Checkout' AND 
                (julianday('now') - julianday(
                    CASE 
                        WHEN instr(h.ActionDate, ' ') > 0 THEN h.ActionDate
                        ELSE h.ActionDate || ' 00:00:00'
                    END
                )) > 3 AND 
                NOT EXISTS (
                    SELECT 1
                    FROM History h2
                    WHERE h2.BookID = h.BookID 
                      AND h2.UserID = h.UserID 
                      AND h2.Action = 'Book Returned' 
                      AND julianday(h2.ActionDate) > julianday(h.ActionDate)
                )
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            cursor.close()

            # Print out the raw results for debugging
            print("Raw Results from Query:")
            for row in results:
                print(row)

            late_books = []
            for result in results:
                late_books.append({
                    'book_id': result[0],
                    'title': result[1],
                    'author': result[2],
                    'genre': result[3],
                    'user_id': result[4],
                    'username': result[5],
                    'days_late': int(result[6])
                })

            # Print out the processed late_books list for debugging
            print("Processed Late Books List:")
            for book in late_books:
                print(book)

            return late_books

        except sqlite3.Error as e:
            print(f"Error fetching late books: {e}")
            return []

    def run_report(self, date_of_action=None, action_type=None, username=None):
        query = """
            SELECT 
                h.HistoryID, 
                h.BookID, 
                u.UserName, 
                h.Action, 
                h.ActionDate, 
                h.SupportMessageID
            FROM History h
            JOIN Users u ON h.UserID = u.UserID
        """
        conditions = []
        params = []

        if date_of_action:
            conditions.append("DATE(h.ActionDate) = ?")
            params.append(date_of_action)

        if action_type:
            conditions.append("h.Action = ?")
            params.append(action_type)

        if username:
            conditions.append("u.UserName = ?")
            params.append(username)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    def get_all_actions(self):
        query = "SELECT DISTINCT Action FROM History"
        cursor = self.conn.cursor()
        cursor.execute(query)
        actions = cursor.fetchall()
        cursor.close()

        return [action[0] for action in actions]
