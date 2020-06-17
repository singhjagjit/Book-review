# Book review website

> "This is a book review website. Users can register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. This website also uses a third-party API by Goodreads, a book review website, to pull in ratings from a broader audience. Finally, users can query for book details and book reviews programmatically via website’s API."

__[Project Demonstration - Youtube Video](https://youtu.be/ysvqGtt4oaE)__


### Technologies Used:
* Flask
* HTML
* CSS
* PostgreSQL
* API


### Description of the files:

* __forms.py__
    * to create login and registration form for the web application.
    * installed flask-wtf package.
    * used wtforms and wtforms.validators

* __application.py__
    * register() function
        * validates the registration form.
        * checks if user already exists.
        * uses flash function to show suitable messages.
        * returns register.html
    
    * login() function
        * validates the login form.
        * check if username and password matches.
        * uses flash function to show suitable messages.
        * returns login.html
    
    * search() function
        * returns search.html if user is logged in
        * returns error.html if user tries to access search page without logging in.

    * books() function
        * returns books.html and shows list of books based on user's input.
        * returns error.html if user's input doesn't match any book in list.

    * book(isbn) function
        * requests goodreads api.
        * stores users' reviews in database and show on webpage.
        * checks if user has already submitted the review.
        * returns book.html and show all the required information of a particular book.

    * book_api(isbn) function
        * returns data about a book in JSON format.
    
    * logout() function
        * logout the user and redirect him to the registration page.

* __import.py__
    * takes books form .csv file and imports them to the postgreSQL database.
    * creates three tables: books, users and reviews.
    * books table stores isbn, title, author and year of all the books.
    * users table stores username, user id and password.
    * reviews table stores review id, review, rating, username and isbn of the book.

* __HTML__
    * layout.html
    * register.html
    * login.html
    * search.html
    * books.html
    * book.html
    * error.html

* __CSS__
    * main.css
    
    
    
    

