# CST8319_Group1

# Welcome to Dewey DB Library!

Thank you for showing interest in our Dewey DB Library application designed my Group 1. Below is a brief description and overview of the application. Please note overall the application is designed 
using the REST Framework and MVC design pattern. This application is a simple library application with role based access. The roles are either customer or librarians and each are given different options on what they can see and perform. All html pages are rendered using REST endpoints via the app.py. Each controller then passes on user input to their respective DAO classes. All application activity is tracked via the History table using Activity Dao methods. Note every app.py REST API is secured with a conditional check for session user, if the user is not in session they will be redirect to login_redirect.html where javascript auto_redirect.js will redirect the user back to the login endpoint. All user display messages were achieved by using the Flask Flash object in the endpoints and htmls.

# How to Install Dewey DB Library

How to Install Dewey DB Library

PyCharm IDE - Git Project
Note if not installed already, download and install Python 3.8 from https://www.python.org/downloads/

First access Pycharm IDE, if prompted when opening pycharm select get from VCS or select the git option on the top tray once you have created your new project. From there, Select Clone and the URL will be https://github.com/lindsaycharlotte/CST8319_Group1. 

Once successfully cloned you will need to add your python interpreter. Go to File on the top, settings. On the next window look for Project:CST8319Group_1 and expand the options.

If Microsoft Defender warning pops up please select Automatically, or click on the botton tray of Pycharm to allow, otherwise it may slow the download process.

Next select the Python Interpreter option and on the right side you should see Python Interpreter: and its probably highlighted red. On the right simply click Add Interpreter -> Add Local Interpreter. Make sure your python locations are entered and are likely
already prefilled. Click ok, now wait a few mins and let the indexes and environment load.

Next go to the requirements.txt file in the root directory of the project. Once you click on that you should see blue text towards the top right saying install dependencies, click that link and let all the dependencies install.

If you do not see a blue link, simply go to the terminal tab on the botton edge of Pycharm and paste this command in and press enter pip install -r requirements.txt

Once completed, locate the app.py file in the root of the project, right click and click run. Once loaded got to localhost:5000 and explore the application!


Docker Method, If you do not have docker installed please refer to https://docs.docker.com/engine/install/ for instructions on how to use Docker

Without having to install PyCharm you can just run it as a container!

Windows PowerShell Method 

Extract the zip contents and via PowerShell navigate to where you extracted the folder CST8319_Group1 and run the below command:

docker build -t group1demo .; docker run -d -p 5000:5000 group1demo

Then simply navigate to localhost:5000 and explore the site with either 
User: user1 or user2 or user3
Password: 1 , for both

Linux Ubuntu Method 

If you wish to run in a VM simply extract the zip to your home folder, then in terminal navigate to where you extracted and run the below command:

docker build -t group1demo . && docker run -d -p 5000:5000 group1demo

Then simply navigate to localhost:5000 and explore the site with either 
User: User: user1 or user2 or user3
Password: 1 , for both

# Secure Login and Registration (Account Creation)

Each html page an endpoint secured with conditional statements that ensure a user is in fact logged in. If the user is not logged in they will be redirected to a page login_redirect page accompanied with our redirect javascript,, will
countdown in real time from 3 seconds. Once the time has allotted the user will be redirect back to the login page.

This application offers secure login where a unique session token is created upon each successful login. Passwords are secured by enforcing IEEE Password standards upon new users registration. 
This will be the first page you see when starting the application, it is a simple form that allows users to enter their username and password to perform a login validation. This page will also contain our privacy policy and our terms and conditions. This area also includes a hyper link to create aa new user via registartion and an option to recover your password via the forgot password link. 
The end points that facilitate overall user access are below

Login


def login() provides the login page rendering and also with its accompanying UserDao method def authenticate_user upon submission 
of the username and password
def logout() used to clear session token which allows users to end their session in the application.

Registration

app.py def register renders register.html where the user will be shown a simple form that allows users to fill out their account information for registration.
This same endpoint performs registration with UserDao def create_user which performs the insert to create a user account
Registration page also uses password_check.js to ensure accounts are created using IEEE Standard passwords.

Password Recovery

app.py def forgot_password() Renders forgot_Password.html with a simple form that requests the users, username and email
app.py def forgot_password() also does forgot password function and is accompanied by UserDao def change_password method, this is activated as 
a POST once the user submits the form, it simulates sending an email but for now the password is just sent via a print statement.

# Display Books, Checking Out Books, Returning Books and Search Books

The next section is the books.html page. After successful login this page will display all books currently available in the inventory. From here users will be able to search for books, checkout books, and return books. This page also contains logic to ensure the book is marked as unavailable once a user checks a book out and also ensures only that user may return it. The supporting endpoints, htmls and daos are below:

Displaying books and Search Books

app.py def book_page() renders the books.html page and also performs conditional logic for searching books, accompanied by BookDao def get_all_books, searching is handled by the BookDao method def search_books. Search function is very basic and is just as LIKE statment for every field name so results are not exact.

Checking Out Books

app.py def book_page performs logic to check a book out and mark as unavailable, accompanied by BookDao method  def checkout_book. 
Upon the user clicking the checkout button next to the book displayed the endpoints will trigger. It will first make sure the book is 
available and if available it will perform the necessary CRUD operations to record the user checking out a book.

Returning Books

Returning books is handled by the app.py  endpoint def book_page which works with Book Dao method def return_book.
First it checks that the user that clicks the return button on the html table on books.html is the same user as checkout, 
if so the function will continue and update the database setting the book to available and recording the user returning the book back to inventory.

# Book Details, and Rate Books

Users can also rate their books and provide text based reviews via the books.html page by simply clicking on the Book id. From here users can 
select a 1 to 5 rating and leave their feedback on the books. Via this section the user will also see a close up details of the book. 

Book Details

app.py def book_details renders the html that allows you to see close up of book, uses dao method def get_book_by_id to get book data

Rate Book

app.py def book_details is the endpoint that handles the rating logic, uses BookDao method def add_rating() for SQL logic

# Order Books, Wishlist/Waitlist

Depending on user role the order_book.html will give you different options. If user is a librarian this is where they can order new books and add 
them to the available stock for customers. If the user is a customer then this is where they can add books to their wishlist. This section contains
alot of logic to ensure that books loaded on this page do not exist on the books table already.

Order Books

app.py def order_book renders the order_books.html page to accomodate both roles this endpoint uses both BookDao method def get_books_not_in_library 
to ensure only books not in stock are rendered on this page, this endpoint also uses WishListDao method def get_wishlist_by_user and def book_in_wishlist to ensure that only books not in stock and not already in the customers wishlist are loaded

# Manage Account, Admin Management, Customer Fines/ Late Fees, Reporting Functionality

This section is located on dashboard.html and utilizes JQuery to organize all HTML tables into their own tab. For a user who is a customer they will
see tabs Your Account Info, Your Wishlist, Your History, and Your Late Books. If the user is a librarian they will see tabs All Users, All Users Borrowing History, All Users Late Books, and Run Reports. The first tabs allow for users and admins to manage the accounts and update users passwords as desired. The borrowing history tabs allows a user to see their history or an admin to see all user history to review activity. Late fees tabs will show a user any books that are past due > 1 day since checkout without a Book Return that is > than the Book Checkout action date. If user is a librarian they will see one additional tab called Run Reports, this allows librarians to run a query based on either Action date, action or user. When a librarian clicks run report they will then be redirected to report_data.html where they can view or export the data as CSV.

app.py def dashboard renders the HTML page dashboard.html which gives the tabbed view. Jquery is located at dashboard.js with css dashboardcss.css 
to allow the grouping of tabs. 

Customer

If the user is a customer the following daos and their methods are used. UserDao def get_user_by_username. This allows a customer to see their
account info and update their password if desired. When the user clicks change password they will be redirected to the change_password.html which is rendered by app/py def change_password, from here a user can enter their new password and click submit, this will then activate UserDao method def change_password. The wishlist tab is loaded via WishlistDao def update_book_availability get_wishlist_by_user. This allows the users own custom wishlist to be displayed. The update availablity method allows the html to be updated to show when a book in their wishlist is now in stock at the library, the users also have a delete option where they can remove items from their wishlist via the app.py def remove_from_wishlist and WishlistDao def remove_book_from_wishlist , HistoryDao def get_history_by_user(user_id) with BookDao get_book_by_id and get_book_name to populate the users history. Def get_late_books() from HistoryDao is used to calculate and determine what books are marked as late and placed into the html table in the Late Fees tab. 

Librarian  

If the user is a librarian then the following Daos and methods are used. UserDAO def get_all_users is used to list all the users for All users tab.
As a librarian the user will have one extra button oppose to change password, they will also be able to delete a user using app.py endpoint def delete_user and UserDao def delete_user. A combination of User Dao def get_userid and def get_username are used to faciltate the query from HistoryDao called def get_history_by_user. THis allows us to loop and display all users history. For all users late fees we first used the HistoryDao method def get_late_books and then call the UserDao method get all users and load up the users variable to be looped and read by the dashboard.html page. The run report tab is run by app.py endpoint def run_report which allows the form on dashboard.html to post and generate a report based on the prompts select using HistoryDao method def run_report, the prompts are preloaded using the UserDao method def getallusers and the actions are preloaded using the def get_all_actions so the user can select from preexisting values to query against. The results are then rendered in an HTML table on report_data.html. On this page the user can either go back to dashboard.html via the go back button or they can export the results to a csv. The exporting is handled via app.py method def export_csv.

# Customer Assistance, Book Requests

This section consists of the support.html and support_detail.html. On the support page if the user is a customer they will be able to create a ticket and they will be able to see a list of all tickets that were opened by them. If the user is a librarian they will not have the create ticket option and can see every ticket created in the system.  On that page if you click the ID it will open the support_detail.html page which will give a close up of the ticket. If a user is a customer they will be able to add a comment and update the ticket, this is recorded by user, role, and time to allow for communication between customer and librarian. If the user is a librarian they will also be able to update the ticket but will have an additional feature that allows them to update the state of the ticket.

User

app.py method def support() renders the initial html page support.html. Initially the UserDAO method def get_user_by_id is called so we can check 
the users role.

Customer

If the user is a customer the Support Dao method def get_tickets_by_user is called and the html table is populated with tickets they created. 
A customer will also have an option to click create ticket on this page which calls the app.py method def create_ticket,
this renders an html page called create_ticket.html and also serves as our Post endpoint for the form. Upon submission of the form the SupportDao
method create_support_message is called to create the ticket. From there the customer can click on the id and 
app.py method def support_detail renders the support_detail.html. This method also uses UserDAO but instead def get_user_by_username so we can 
populate user updates with the actual user name and not just the id. Next the SupportDao method def get_ticket_by_id is called to get the ticket
details and the def get_support_comments to generate the comments for the ticket. From here the user can provide updates to the tickets via a 
text box form and when they click update the app.py method def support_detail is called which calls the SupportDao method def add_support_comment.

Librarian

For a librarian all is the same except on page render of support.html via app.py def support SupportDao method get_all_tickets is called and a list
of all available tickets are shown, a librarian does not have the option to create a ticket.

When entering support_detail.html a librarian will have the additional option of updating the status of a ticket.
This is done by calling the same app.py def support_detail method but it calls the SupportDao method def update_ticket_status for the librarian role ,
this allows librarians to close the ticket once assistance isnt required.
