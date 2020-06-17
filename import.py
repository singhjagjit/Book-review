import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL)")
db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, review VARCHAR NOT NULL, rating INTEGER NOT NULL, username VARCHAR NOT NULL, isbn VARCHAR NOT NULL)")

f = open("books.csv")
reader = csv.reader(f)
for isbn, title, author, year in reader:
    if year == "year":
        continue
    else:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
db.commit()

