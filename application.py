import os
import requests

from flask import Flask, session, render_template, url_for, flash, redirect, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config['SECRET_KEY'] = 'aef6f23ec696d04bf2a3b6e407f92ae8'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data

        data = db.execute("SELECT username from users WHERE username = :username", {"username": user}).fetchall()

        if not data:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": user, "password": password})
            db.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))

        else:
            flash(f'Username already exists!', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data

        data = db.execute("SELECT username, password from users WHERE username = :username AND password = :password", {"username": user, "password": password}).fetchall()

        if not data:
            flash(f'Username/Password does not match!', 'danger')
            return redirect(url_for('login'))

        else:
            user = form.username.data
            session["user"] = user
            flash('You have been logged in!', 'success')
            return redirect(url_for('search'))

    return render_template('login.html', form=form)



@app.route("/search", methods=['GET', 'POST'])
def search():
    if "user" in session:
        user = session["user"]
        return render_template('search.html')
    else:
        return render_template('error.html', message="Please register or login first")



@app.route("/books", methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        search_term = request.form.get("search_term")

        books = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :term OR title LIKE :term OR author LIKE :term OR year LIKE :term", {'term': '%'+search_term+'%'})

        if books.rowcount == 0:
            return render_template('error.html', message="No result found, try different keywords.")
        else:
            return render_template('books.html', books=books)

    else:
        return render_template('error.html', message="Please register or login first")



@app.route("/books/<string:isbn>", methods=['GET', 'POST'])
def book(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "WphoyKAygslgoJrbAVXA", "isbns": isbn})

    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    numOfRatings = data["books"][0]["work_ratings_count"]
    avgRating = data["books"][0]["average_rating"]

    book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchone()
    book_reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()

    if request.method == 'POST':
        user = session["user"]
        rating = request.form.get("rating")
        review = request.form.get('review')
        user_reviews = db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": user, "isbn": isbn}).fetchall()

        if user_reviews:
            return render_template('book.html',book=book, reviews=book_reviews, message="Review already submitted!!", numOfRatings=numOfRatings, avgRating=avgRating)

        else:
            db.execute("INSERT INTO reviews (review, rating, username, isbn) VALUES (:review, :rating, :username, :isbn)", {"review": review, "rating": rating, "username": user, "isbn": isbn})
            db.commit()
            book_reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
            return render_template('book.html', book=book, reviews=book_reviews, message="Review submitted successfully!!", numOfRatings=numOfRatings, avgRating=avgRating)

    return render_template('book.html', book=book, reviews=book_reviews, numOfRatings=numOfRatings, avgRating=avgRating)



@app.route("/api/<string:isbn>")
def book_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchone()

    if book is None:
        return jsonify({"404 error": "Page not found"}), 404

    title = book.title
    author = book.author
    year = int(book.year)
    isbn = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "WphoyKAygslgoJrbAVXA", "isbns": isbn})

    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    numOfRatings = data["books"][0]["work_ratings_count"]
    avgRating = data["books"][0]["average_rating"]
    avgRating = float(avgRating)

    return jsonify(
        {
            "title": title,
            "author": author,
            "year": year,
            "isbn": isbn,
            "review_count": numOfRatings,
            "average_score": avgRating
        }
    )

    

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash('You are logged out!', 'success')
    return redirect(url_for('register'))