import csv
import os
import sqlite3
import uuid
from datetime import datetime

from flask import Flask, render_template, redirect, session, request, url_for, flash, json, make_response, Response, \
    get_flashed_messages

from bean.User import User
from dao.ActivityDao import ActivityDao
from dao.BookDao import BookDao
from dao.HistoryDao import HistoryDao
from dao.SupportDao import SupportDao
from dao.UserDao import UserDao
from dao.WishlistDao import WishlistDao
from model.DB_init import DB_init
from model.merchantAPI import *

app = Flask(__name__)
db_init = DB_init(app)

# Initialize the database and generate test data
db_init.init_db()
with app.app_context():
    db_init.init_db()
    db_init.insert_data()

app.secret_key = str(uuid.uuid4())  # Random UUID Token


# Register page rendering and its functionalities
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle POST request: form submission for registration
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        role = 'customer'

        if not (username and email and password):
            return "Username, email, and password are required."

        conn = sqlite3.connect('library.db')
        user_dao = UserDao(conn)

        if user_dao.create_user(username, email, phone, password, role):
            activity_dao = ActivityDao(conn)
            user = user_dao.get_user_by_username(username)
            user_id = user.get_userid()
            activity_dao.log_activity(user_id, "User Created")
            return redirect(url_for('login'))
        else:
            return "Error registering user."
    else:
        # Handle GET request: render the registration page
        return render_template('register.html')


@app.route('/forgot_password.html', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        conn = sqlite3.connect('library.db')
        user_dao = UserDao(conn)

        result = user_dao.forgot_password(username, email)

        if result:
            password = result[0]
            print(f"The password for user {username} is: {password}")

        conn.close()
        return redirect(url_for('login'))

    return render_template('forgot_password.html')


# Login page rendering and its functionalities, merged
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)

    if request.method == 'POST':
        # Handle POST request: form submission for login
        username = request.form['uname']
        password = request.form['psw']
        user = user_dao.authenticate_user(username, password)
        if user:
            # Successful login, store session data
            session['user_id'] = user.get_userid()
            session['username'] = user.get_username()
            session['user_role'] = user.get_role()
            activity_dao = ActivityDao(conn)
            activity_dao.log_activity(session['user_id'], "login")
            conn.close()  # Close the connection after use
            return redirect(url_for('book_page'))  # Redirect to the desired page
        else:
            error_message = "Invalid username or password"

    conn.close()  # Close the connection after use
    return render_template('login.html', error_message=error_message)


@app.route('/terms_of_service.html')
def terms_of_service():
    return render_template('terms_of_service.html')


@app.route('/privacy_policy.html')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/logout')  # Logout functionality, cancels session
def logout():
    conn = sqlite3.connect('library.db')
    activity_dao = ActivityDao(conn)
    activity_dao.log_activity(session['user_id'], "logout")
    #clear by querying
    get_flashed_messages(with_categories=False)

    session.pop('username', None)
    session.pop('user_role', None)
    session.pop('user_id', None)

    return redirect(url_for('login'))


# OrderPage Wishlist with adding to libnrary and adding to wishlist and page rendering mereged to one endpoint
@app.route('/order_book', methods=['GET', 'POST'])
def order_book():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        # Branch id only used in add book feature as librarian
        if 'branch_id' in request.form:
            # Handle adding a new book to the library
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            branch_id = request.form['branch_id']

            conn = sqlite3.connect('library.db')
            book_dao = BookDao(conn)
            activity_dao = ActivityDao(conn)

            book_dao.add_book(title, author, genre, branch_id)
            new_book = book_dao.get_book_by_title(title)
            book_id = new_book.get_book_id()
            activity_dao.log_activity_book(session['user_id'], "Added Book", book_id)

            conn.close()
            flash(f'Book "{title}" by {author}, genre: {genre}, branch ID: {branch_id} added successfully!')
            return redirect(url_for('order_book'))
        # Assume if these 3 fields are included its a wishlist post
        elif 'title' in request.form and 'author' in request.form and 'genre' in request.form:
            # Handle adding a book to the wishlist
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            user_id = session['user_id']

            conn = sqlite3.connect('library.db')
            wishlist_dao = WishlistDao(conn)
            activity_dao = ActivityDao(conn)

            if wishlist_dao.book_in_wishlist(user_id, title, author, genre):
                flash("Book is already in your wishlist.")
            else:
                wishlist_dao.add_book_to_wishlist(user_id, title, author, genre)
                flash("Book added to wishlist.")
                activity_dao.log_activity(user_id, "Added to Wishlist")

            conn.close()
            return redirect(url_for('order_book'))

    # For requests not related to adding books or wishlist
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    search_query = request.args.get('search', '').strip()

    conn = sqlite3.connect('library.db')
    book_dao = BookDao(conn)
    wishlist_dao = WishlistDao(conn)

    # Fetch books not in the user's wishlist with search query
    books_to_render = book_dao.get_books_not_in_library(search_query)
    user_wishlist = set(wishlist_dao.get_wishlist_by_user(user_id))

    conn.close()

    return render_template('order_book.html', books=books_to_render, role=user_role, wishlist=user_wishlist)


# Book page rendering and its functionalities
@app.route('/books.html', methods=['GET', 'POST'])
def book_page():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return render_template('login_redirect.html')

    conn = sqlite3.connect('library.db')
    book_dao = BookDao(conn)
    user_dao = UserDao(conn)
    activity_dao = ActivityDao(conn)

    if request.method == 'POST':
        # Handle checkout or return book actions
        book_id = request.form.get('book_id')
        action = request.form.get('action')
        user_id = session['user_id']

        if book_id and action:
            if action == 'checkout':
                if book_dao.checkout_book(book_id, user_id):
                    flash('Book checked out successfully!', 'success')
                    activity_dao.log_activity_book(user_id, "Book Checkout", book_id)
                else:
                    flash('Book is not available or an error occurred.', 'error')
            elif action == 'return':
                if book_dao.return_book(book_id, user_id):
                    flash('Book returned successfully!', 'success')
                    activity_dao.log_activity_book(user_id, "Book Returned", book_id)
                else:
                    flash('You cannot return this book or an error occurred.', 'error')

        conn.close()
        return redirect(url_for('book_page'))

    # For GET requests
    search_query = request.args.get('search', '').strip()

    if search_query:
        books = book_dao.search_books(search_query)
    else:
        books = book_dao.get_all_books()

    conn.close()
    return render_template('books.html', books=books)


# Book details page functions rate and view details merged into one endpoint
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login'))

    conn = sqlite3.connect('library.db')
    book_dao = BookDao(conn)
    user_dao = UserDao(conn)
    activity_dao = ActivityDao(conn)

    if request.method == 'POST':
        # Handle rating submission
        rating = request.form['rating']
        review = request.form['review']

        # Fetch user by username
        user = user_dao.get_user_by_username(session['username'])
        user_id = user.get_userid()

        # Add rating to the database
        book_dao.add_rating(user_id, book_id, rating, review)

        # Log the activity
        activity_dao.log_activity_book(session['user_id'], "Rating Added", book_id)

        conn.close()

        return redirect(url_for('book_details', book_id=book_id))

    # For GET requests: Display book details and reviews
    book = book_dao.get_book_by_id(book_id)
    reviews = book_dao.get_ratings_by_book(book_id)

    reviews_with_username = []
    for review in reviews:
        review_with_username = {
            'username': review[1],
            'rating': review[2],
            'review_text': review[3]
        }
        reviews_with_username.append(review_with_username)

    conn.close()
    return render_template('book_detail.html', book=book, reviews=reviews_with_username)


@app.route('/dashboard.html')
def dashboard():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return render_template('login_redirect.html')

    username = session['username']
    user_role = session['user_role']
    user_id = session['user_id']
    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)
    wishlist_dao = WishlistDao(conn)
    history_dao = HistoryDao(conn)
    book_dao = BookDao(conn)
    actions = history_dao.get_all_actions()

    if user_role == 'customer':
        customer_details = user_dao.get_user_by_username(username)
        wishlist_dao.update_book_availability()
        wishlist = wishlist_dao.get_wishlist_by_user(user_id)

        history_entries = history_dao.get_history_by_user(user_id)
        for entry in history_entries:
            book = book_dao.get_book_by_id(entry.get_book_id())
            if book:
                entry.book_title = book.get_book_name()
            else:
                entry.book_title = "N/A"

        late_books = history_dao.get_late_books_by_user(user_id)  # Fetch late books
        print(late_books)

        conn.close()
        return render_template(
            'dashboard.html', user=customer_details, user_role=user_role,
            wishlist=wishlist, history=history_entries, late_books=late_books
        )
    elif user_role == 'librarian':
        users = user_dao.get_all_users()
        all_users_history = {}

        for user in users:
            user_id = user.get_userid()
            user_name = user.get_username()
            all_users_history[user_name] = history_dao.get_history_by_user(user_id)

        late_books = history_dao.get_late_books()  # Fetch late books
        users = user_dao.get_all_users()

        conn.close()
        return render_template(
            'dashboard.html', users=users, user_role=user_role,
            all_users_history=all_users_history, late_books=late_books, actions=actions)


@app.route('/run_report', methods=['POST'])
def run_report():
    if 'username' in session:  # Ensure user is logged in
        # Extract form data
        date_of_action = request.form.get('date_of_action')
        action_type = request.form.get('action_type')
        username = request.form.get('username')

        conn = sqlite3.connect('library.db')
        history_dao = HistoryDao(conn)

        # Process the data and generate report
        report_data = history_dao.run_report(date_of_action, action_type, username)

        conn.close()

        if report_data:
            # Render the report data as HTML
            return render_template('report_data.html', report_data=report_data)
        else:
            flash("No report data found matching the criteria.")
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/export_csv', methods=['POST'])
def export_csv():
    if 'username' in session:  # Ensure user is logged in
        # Extract report data from the request form
        report_data = request.form.getlist('report_data[]')

        if report_data:
            # Create CSV content with specific fields
            csv_content = "HistoryID,BookID,UserID,Action,ActionDate,SupportMessageID\n"
            for data in report_data:
                csv_content += data + "\n"

            # Return CSV file as response
            return Response(
                csv_content,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=report_data.csv"}
            )
        else:
            flash("No report data available for export.", 'error')
            return redirect(url_for('run_report'))  # Redirect to the report generation page
    else:
        return redirect(url_for('login'))  # If no user session, redirect to login


@app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        user_dao.change_password(user_id, new_password)
        conn.commit()
        conn.close()
        flash("Password successfully updated!")
        activity_dao = ActivityDao(conn)
        activity_dao.log_activity(session['user_id'], "Password Changed")
        return redirect(url_for('dashboard'))

    # For GET requests, render the change password form
    user = user_dao.get_user_by_id(user_id)
    conn.close()
    return render_template('change_password.html', user=user)


@app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    wishlist_id = request.form.get('wishlist_id')
    conn = sqlite3.connect('library.db')
    wishlist_dao = WishlistDao(conn)
    wishlist_dao.remove_book_from_wishlist(wishlist_id)
    activity_dao = ActivityDao(conn)
    activity_dao.log_activity(session['user_id'], "Removed from Wishlist")
    flash("Book removed from wishlist!")
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)
    user_dao.delete_user(user_id)
    activity_dao = ActivityDao(conn)
    activity_dao.log_activity(session['user_id'], "Removed User " + str(user_id))
    conn.close()

    flash("User successfully deleted!")
    return redirect(url_for('dashboard'))


# Support page rendering
@app.route('/support.html')
def support():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    user_role = session['user_role']
    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)
    support_dao = SupportDao(conn)
    username = session['username']
    user = user_dao.get_user_by_username(username)
    user_id = user.get_userid()

    if user_role == 'customer':
        tickets = support_dao.get_tickets_by_user(user_id)
        conn.close()
        return render_template('support.html', user=user, user_role=user_role, tickets=tickets)

    elif user_role == 'librarian':
        tickets = support_dao.get_all_tickets()
        conn.close()
        return render_template('support.html', user=user, user_role=user_role, tickets=tickets)


# Support Details page rendering and its functionalities
@app.route('/support_detail/<int:support_id>', methods=['GET', 'POST'])
def support_detail(support_id):
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login_page'))

    user_role = session['user_role']
    user_id = session['user_id']
    conn = sqlite3.connect('library.db')
    user_dao = UserDao(conn)
    support_dao = SupportDao(conn)
    activity_dao = ActivityDao(conn)
    username = session['username']
    user = user_dao.get_user_by_username(username)
    ticket = support_dao.get_ticket_by_id(support_id)
    comments = support_dao.get_support_comments(support_id)

    if not ticket:
        flash("Ticket not found.")
        conn.close()
        return redirect(url_for('support'))

    if request.method == 'POST':
        if user_role == 'librarian':
            # Handle status updates for librarians
            new_status = request.form.get('update_status')
            if new_status in ['open', 'closed']:
                support_dao.update_ticket_status(support_id, new_status)
                activity_message = "ticket opened" if new_status == "open" else "ticket closed"
                activity_dao.log_activity(user_id, activity_message)
                flash("Ticket status updated successfully.")
            else:
                flash("Invalid status value.")
        # else all users can comment on tickets
        update_text = request.form.get('update_text')
        if update_text:
            support_dao.add_support_comment(support_id, user_id, update_text)
            activity_dao.log_activity_support(user_id, "ticket commented", support_id)
            flash("Comment added successfully.")

        conn.close()
        return redirect(url_for('support_detail', support_id=support_id))

    conn.close()
    return render_template('support_detail.html', user=user, user_role=user_role, ticket=ticket, comments=comments)


# Create page rendering and its functionality
@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'GET':
        if session['user_role'] == 'customer':
            return render_template('create_ticket.html')
        else:

            return redirect(url_for('support'))

    elif request.method == 'POST':
        if session['user_role'] == 'customer':
            subject = request.form['subject']
            message_text = request.form['message_text']
            user_id = session['user_id']
            conn = sqlite3.connect('library.db')
            support_dao = SupportDao(conn)
            ticket = support_dao.create_support_message(user_id, subject, message_text)

            activity_dao = ActivityDao(conn)
            activity_dao.log_activity_support(session['user_id'], "Ticket Created", ticket)
            return redirect(url_for('support'))
        else:

            return redirect(url_for('support'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)

