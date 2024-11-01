from flask import Flask, render_template, jsonify, request, make_response, abort#import flask libraries
import os
import sqlite3

app = Flask(__name__)

def initialize_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            description TEXT,
            is_read TEXT NOT NULL DEFAULT 'N',
            current_book TEXT NOT NULL DEFAULT 'N',
            rating TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user TEXT,
            review TEXT,
            rating TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

@app.route('/')
def home_form():
    return render_template('home.html')

@app.route('/books/', methods = ['GET']) 
def get_books():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        books = cursor.execute("SELECT * FROM books").fetchall()
        review_counts = {}
        for book in books:
            review_query = "SELECT COUNT(*) FROM reviews WHERE book_id = ?"
            review_count = cursor.execute(review_query, (book[0],))
            review_count = review_count.fetchone()
            review_counts[book[0]] = review_count[0]
        final_json_response = []
        for book in books:
            json_response = {}
            json_response["id"] = book[0]
            json_response["title"] = book[1]
            json_response["author"] = book[2]
            json_response["genre"] = book[3]
            json_response["description"] = book[4]
            json_response["is_read"] = book[5]
            json_response["current_status"] = book[6]
            if review_counts[book[0]] > 0:
                reviews = []
                review_query = "SELECT * FROM reviews WHERE book_id = ?"
                book_reviews = cursor.execute(review_query, (book[0],)).fetchall()
                for review in book_reviews:
                    review_response = {}
                    review_response["id"] = review[0]
                    review_response["book_id"] = review[1]
                    review_response["review"] = review[2]
                    reviews.append(review_response)
                json_response["reviews"] = reviews  
            else:
                json_response["reviews"] = []
            final_json_response.append(json_response)

        if request.headers.get('Accept') == 'application/json':
            conn.close()
            return jsonify(final_json_response)
        else:
            conn.close()
            return render_template('bookUI.html', books=books, review_counts=review_counts)
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

    

@app.route('/books/read', methods = ['GET']) 
def get_read_books():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        books = cursor.execute("SELECT * FROM books WHERE is_read = 'Y'").fetchall()
        review_counts = {}
        for book in books:
            review_query = "SELECT COUNT(*) FROM reviews WHERE book_id = ?"
            review_count = cursor.execute(review_query, (book[0],))
            review_count = review_count.fetchone()
            review_counts[book[0]] = review_count[0]
        if request.headers.get('Accept') == 'application/json':
            final_json_response = []
            for book in books:
                json_response = {}
                json_response["id"] = book[0]
                json_response["title"] = book[1]
                json_response["author"] = book[2]
                json_response["genre"] = book[3]
                json_response["description"] = book[4]
                json_response["is_read"] = book[5]
                json_response["current_status"] = book[6]
                if review_counts[book[0]] > 0:
                    reviews = []
                    review_query = "SELECT * FROM reviews WHERE book_id = ?"
                    book_reviews = cursor.execute(review_query, (book[0],)).fetchall()
                    for review in book_reviews:
                        review_response = {}
                        review_response["id"] = review[0]
                        review_response["book_id"] = review[1]
                        review_response["message"] = review[2]
                        reviews.append(review_response)
                else:
                    json_response["reviews"] = []
                final_json_response.append(json_response)

            conn.close()
            return jsonify(final_json_response)
        else:
            conn.close()
            return render_template('readBookUI.html', books=books, review_counts=review_counts)
        
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
@app.route('/books/unread', methods = ['GET']) 
def get_unread_books():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        books = cursor.execute("SELECT * FROM books WHERE is_read = 'N'").fetchall()
        review_counts = {}
        for book in books:
            review_query = "SELECT COUNT(*) FROM reviews WHERE book_id = ?"
            review_count = cursor.execute(review_query, (book[0],))
            review_count = review_count.fetchone()
            review_counts[book[0]] = review_count[0]
        if request.headers.get('Accept') == 'application/json':
            final_json_response = []
            for book in books:
                json_response = {}
                json_response["id"] = book[0]
                json_response["title"] = book[1]
                json_response["author"] = book[2]
                json_response["genre"] = book[3]
                json_response["description"] = book[4]
                json_response["is_read"] = book[5]
                json_response["current_status"] = book[6]
                if review_counts[book[0]] > 0:
                    reviews = []
                    review_query = "SELECT * FROM reviews WHERE book_id = ?"
                    book_reviews = cursor.execute(review_query, (book[0],)).fetchall()
                    for review in book_reviews:
                        review_response = {}
                        review_response["id"] = review[0]
                        review_response["book_id"] = review[1]
                        review_response["message"] = review[2]
                        reviews.append(review_response)
                else:
                    json_response["reviews"] = []
                final_json_response.append(json_response)

            conn.close()
            return jsonify(final_json_response)
        else:
            conn.close()
            return render_template('unreadBookUI.html', books=books, review_counts=review_counts)
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

@app.route('/books/current', methods = ['GET']) 
def get_current_book():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        books = cursor.execute("SELECT * FROM books WHERE current_book = 'Y'").fetchall()
        review_counts = {}
        for book in books:
            review_query = "SELECT COUNT(*) FROM reviews WHERE book_id = ?"
            review_count = cursor.execute(review_query, (book[0],))
            review_count = review_count.fetchone()
            review_counts[book[0]] = review_count[0]
        if request.headers.get('Accept') == 'application/json':
            final_json_response = []
            for book in books:
                json_response = {}
                json_response["id"] = book[0]
                json_response["title"] = book[1]
                json_response["author"] = book[2]
                json_response["genre"] = book[3]
                json_response["description"] = book[4]
                json_response["is_read"] = book[5]
                json_response["current_status"] = book[6]
                if review_counts[book[0]] > 0:
                    reviews = []
                    review_query = "SELECT * FROM reviews WHERE book_id = ?"
                    book_reviews = cursor.execute(review_query, (book[0],)).fetchall()
                    for review in book_reviews:
                        review_response = {}
                        review_response["id"] = review[0]
                        review_response["book_id"] = review[1]
                        review_response["review"] = review[2]
                        reviews.append(review_response)
                else:
                    json_response["reviews"] = []
                final_json_response.append(json_response)

            conn.close()
            return jsonify(final_json_response)
        else:
            conn.close()
            return render_template('currentBookUI.html', books=books, review_counts=review_counts)
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
@app.route('/books/<int:book_id>/reviews', methods = ['GET'])
def get_reviews(book_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()
        if book_info is None:
            conn.close()
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "Book not found"}), 404
            else:
                return "<h1>404 Error: Book not found</h1>"
        review_query = "SELECT * FROM reviews WHERE book_id = ?"
        reviews = cursor.execute(review_query, (book_id,)).fetchall()

        if request.headers.get('Accept') == 'application/json':
            final_json_response = []
            for review in reviews:
                review_response = {}
                review_response["id"] = review[0]
                review_response["book_id"] = review[1]
                review_response["review"] = review[2]
                review_response["user"] = review[3]
                review_response["rating"] = review[4]
                final_json_response.append(review_response)
            conn.close()
            return jsonify({"title": book_info[0], "author": book_info[1], "reviews": final_json_response})
        else:
            conn.close()
            return render_template('reviewUI.html', book_id = book_id, book_info=book_info, reviews=reviews)
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

@app.route('/books/add_book')
def book_form():
    try:
        return render_template('addBookUI.html')
    except Exception as error:
        print(f"Error rendering Add Book Page: {error}")
        return f"Error rendering Add Book Page: {error}"

@app.route('/books/add_book', methods = ['POST']) 
def add_book():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        if request.is_json:
            json_form = request.get_json(silent=True)
            if json_form is None or json_form == "":
                return jsonify({"Error": "Request Body is empty"}), 400
            title = json_form.get("title")
            if title is None or title == "":
                return jsonify({"Error": 'title is a required field'}), 400
            author = json_form.get("author")
            if author is None or author == "":
                return jsonify({"Error": 'author is a required field'}), 400
            genre = json_form.get("genre")
            if genre is None or genre == "":
                return jsonify({"Error": 'genre is a required field'}), 400
            desc = json_form.get("description")
            if desc is None:
                return jsonify({"Error": 'description is a required field'}), 400
            is_read = json_form.get("read_status")
            current_book = json_form.get("current_status")
        else:
            title = request.form.get("title")
            author = request.form.get("author")
            genre = request.form.get("genre")
            desc = request.form.get("description")
            is_read = request.form.get("read_status")
            current_book = request.form.get("current_status")

        if is_read is None or is_read == "":
            if current_book is None or current_book == "":
                book_query = f"INSERT INTO books (title, author, genre, description, rating) VALUES (?, ?, ?, ?, 'N/A')"
                cursor.execute(book_query, (title, author, genre, desc))
            else:
                if current_book.upper() in ('Y', 'N'):
                    # add logic for updating any current books to N if the value is Y
                    if current_book.upper() == 'Y':
                        cursor.execute(f"UPDATE books SET current_book = 'N' WHERE current_book = 'Y'") # Update the current book to not being read
                    book_query = f"INSERT INTO books (title, author, genre, description, rating, current_book) VALUES (?, ?, ?, ?, 'N/A', ?)"
                    cursor.execute(book_query, (title, author, genre, desc, current_book.upper()))
                else:
                    if request.headers.get('Content-Type') == 'application/json':
                        conn.close()
                        return jsonify({"Error": "current_book is not 'Y' or 'N'"}), 400
                    else:
                        conn.close()
                        return "<h1>400 Error: current_book is not Y or N</h1>"
        else:
            if is_read.upper() in ('Y', 'N'):
                if current_book is None or current_book == "":
                    book_query = f"INSERT INTO books (title, author, genre, description, rating, is_read) VALUES (?, ?, ?, ?, 'N/A', ?)"
                    cursor.execute(book_query, (title, author, genre, desc, is_read.upper()))
                else:
                    if current_book.upper() in ('Y', 'N'):
                        # add logic for updating any current books to N if the value is Y
                        if current_book.upper() == 'Y':
                            cursor.execute(f"UPDATE books SET current_book = 'N' WHERE current_book = 'Y'") # Update the current book to not being read
                        book_query = f"INSERT INTO books (title, author, genre, description, rating, is_read, current_book) VALUES (?, ?, ?, ?, 'N/A', ?, ?)"
                        cursor.execute(book_query, (title, author, genre, desc, is_read.upper(), current_book.upper()))
                    else:
                        if request.headers.get('Content-Type') == 'application/json':
                            conn.close()
                            return jsonify({"Error": "current_book is not 'Y' or 'N'"}), 400
                        else:
                            conn.close()
                            return "<h1>400 Error: current_book is not Y or N</h1>"
            else:
                if request.headers.get('Content-Type') == 'application/json':
                    conn.close()
                    return jsonify({"Error": "read_status is not 'Y' or 'N'"}), 400
                else:
                    conn.close()
                    return "<h1>400 Error: read_status is not Y or N</h1>"

                
        conn.commit()
        if request.headers.get('Content-Type') == 'application/json':
            conn.close()
            return jsonify({"message": f"{title} by {author} added to the Book Club"})
        else:
            conn.close()
            return f"{title} by {author} added to the Book Club"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
    
@app.route('/books/<int:book_id>/add_review')  # Route to render the form
def review_form(book_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        
        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            conn.close()
            return "<h1>404 Error: Book not found</h1>"

        conn.close()

        return render_template('addReviewUI.html', book_info=book_info, book_id=book_id)
    except Exception as error:
        conn.close()
        print(f"Error: {error}")
        return "<h1>500 Error: An internal error occurred</h1>"

@app.route('/books/<int:book_id>/add_review', methods = ['POST']) 
def add_review(book_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")

    try:
        cursor = conn.cursor()
        if request.is_json:
            json_form = request.get_json(silent=True)
            if json_form is None or json_form == "":
                return jsonify({"Error": "Request Body is empty"}), 400
            review = json_form.get("review")
            if review is None or review == "":
                return jsonify({"Error": 'review is a required field'}), 400
            user = json_form.get("user")
            if user is None or user == "":
                return jsonify({"Error": 'user is a required field'}), 400
            rating = json_form.get("rating")
            if rating is None or rating == "":
                return jsonify({"Error": 'rating is a required field'}), 400
            try:
                rating = float(rating)
            except Exception:
                conn.close()
                return jsonify({"Error": "Rating must be a number between the values of 1-5"}), 400
            if not (rating >= 1.0 and rating <=5.0):
                conn.close()
                return jsonify({"Error": "Rating must be between the values of 1-5"}), 400
            if rating.is_integer():
                rating = int(rating)
            else:
                rating = round(rating, 1)

        else:
            review = request.form["review"]
            user = request.form["user"]
            rating = request.form["rating"]
            rating = float(rating)
            if rating.is_integer():
                rating = int(rating)

        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Content-Type') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"
        review_query = f"INSERT INTO reviews (book_id, review, user, rating) VALUES (?, ?, ?, ?)"
        cursor.execute(review_query, (book_id, review, user, rating))

        # Get the reviews for this book so you can get an average for the ratings and update it in the book table
        ratings_query = "SELECT rating FROM reviews WHERE book_id = ?"
        ratings = cursor.execute(ratings_query, (book_id,)).fetchall()
        ratings = [float(rating[0]) for rating in ratings]

        overall_ratings = sum(ratings)/len(ratings)
        if overall_ratings.is_integer():
            overall_ratings = int(overall_ratings)
        else:
            overall_ratings = "%.1f" % overall_ratings

        overall_ratings_query = "UPDATE books SET rating = ? WHERE id = ?"
        cursor.execute(overall_ratings_query, (overall_ratings, book_id)).fetchone()
        
        conn.commit()

        if request.headers.get('Content-Type') == 'application/json':
            conn.close()
            return jsonify({"message": f"Review added for {book_info[0]} by {book_info[1]}"})
        else:
            conn.close()
            return f"Review added for {book_info[0]} by {book_info[1]}"
        
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
@app.route('/books/<int:book_id>/reviews/<int:review_id>')
def update_review_form(book_id, review_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        
        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            conn.close()
            return "<h1>404 Error: Book not found</h1>"

        # Get rating so it can be set to the default on the rating slider
        rating_query = "SELECT rating FROM reviews where id = ?"
        rating = cursor.execute(rating_query, (review_id,)).fetchone()

        if rating is None:
            conn.close()
            return "<h1>404 Error: Review not found</h1>"

        rating = float(rating[0])

        if rating.is_integer():
            rating = int(rating)
        else:
            rating = "%.1f" % rating


        conn.close()

        return render_template('updateReviewUI.html', book_info=book_info, book_id=book_id, review_id=review_id, rating = rating)

    except Exception as error:
        conn.close()
        print(f"Error rendering Update Review Page: {error}")
        return f"Error rendering Update Review Page: {error}"
    
@app.route('/books/<int:book_id>/reviews/<int:review_id>', methods = ['POST', 'PUT']) 
def update_review(book_id, review_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        if request.is_json:
            json_form = request.get_json(silent=True)
            if json_form is None or json_form == "":
                return jsonify({"Error": "Request Body is empty"}), 400
            review = json_form.get("review")
            if review is None or review == "":
                return jsonify({"Error": 'review is a required field'}), 400
            rating = json_form.get("rating")
            if rating is None or rating == "":
                return jsonify({"Error": 'rating is a required field'}), 400
            try:
                rating = float(rating)
            except Exception:
                conn.close()
                return jsonify({"Error": "Rating must be a number between the values of 1-5"}), 400
            if not (rating >= 1.0 and rating <=5.0):
                conn.close()
                return jsonify({"Error": "Rating must be between the values of 1-5"}), 400
            
            if rating.is_integer():
                rating = int(rating)
            else:
                rating = round(rating, 1)
        else:
            review = request.form["review"]
            rating = request.form["rating"]
            rating = float(rating)
            if rating.is_integer():
                rating = int(rating)
        
        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Content-Type') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"

        # check to see if review in table
        review_check = "SELECT * FROM reviews WHERE id = ?"
        review_check = cursor.execute(review_check, (review_id,)).fetchone()

        if review_check is None:
            if request.headers.get('Content-Type') == 'application/json':
                conn.close()
                return jsonify({"Error": "Review not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Review not found</h1>"

        review_query = f"UPDATE reviews SET review = ?, rating = ? WHERE id = ?"
        cursor.execute(review_query, (review, rating, review_id))

        # Update overall ratings once review is updated
        ratings_query = "SELECT rating FROM reviews WHERE book_id = ?"
        ratings = cursor.execute(ratings_query, (book_id,)).fetchall()
        ratings = [float(rating[0]) for rating in ratings]

        overall_ratings = sum(ratings)/len(ratings)
        if overall_ratings.is_integer():
            overall_ratings = int(overall_ratings)
        else:
            overall_ratings = "%.1f" % overall_ratings

        overall_ratings_query = "UPDATE books SET rating = ? WHERE id = ?"
        cursor.execute(overall_ratings_query, (overall_ratings, book_id))

        conn.commit()
        conn.close()

        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"message": f"Review {review_id} updated for {book_info[0]} by {book_info[1]}"})
        else:
            return f"Review {review_id} updated for {book_info[0]} by {book_info[1]}"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

@app.route('/books/<int:book_id>/status', methods = ['GET', 'PUT']) 
def update_read_status(book_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()
        book_query = "SELECT title, author, is_read FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Accept') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"

        read_status = book_info[2]
        if read_status == 'Y':
            read_query = f"UPDATE books SET is_read = 'N' WHERE id = ?"
            return_msg = f"Read status for {book_info[0]} by {book_info[1]} updated to No"
        else:
            read_query = f"UPDATE books SET is_read = 'Y' WHERE id = ?"
            return_msg = f"Read status for {book_info[0]} by {book_info[1]} updated to Yes"

        cursor.execute(read_query, (book_id, ))

        conn.commit()
        conn.close()

        if request.headers.get('Accept') == 'application/json':
            return jsonify({"message": return_msg})
        else:
            return return_msg
        
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

@app.route('/books/<int:book_id>/current', methods = ['GET', 'PUT']) 
def update_current_book(book_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:    
        cursor = conn.cursor()

        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Accept') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"

        # First update the existing current book to N
        cursor.execute("UPDATE books SET current_book = 'N' WHERE current_book = 'Y'")

        # Then update the current book with the id
        update_query = f"UPDATE books SET current_book = 'Y' WHERE id = ?"
        cursor.execute(update_query, (book_id, ))

        conn.commit()
        conn.close()

        if request.headers.get('Accept') == 'application/json':
            return jsonify({"message": f"{book_info[0]} by {book_info[1]} updated to the club's current book"})
        else:
            return f"{book_info[0]} by {book_info[1]} updated to the club's current book"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
@app.route('/books/<int:book_id>/reviews/<int:review_id>/delete', methods = ['GET', 'DELETE']) 
def delete_review(book_id, review_id):
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:    
        cursor = conn.cursor()

        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Accept') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"
        
        review_check_query = "SELECT * FROM reviews WHERE book_id = ? AND id = ?"
        review_check = cursor.execute(review_check_query, (book_id, review_id)).fetchone()
        if review_check is None:
            if request.headers.get('Accept') == 'application/json':
                conn.close()
                return jsonify({"Error": "Review not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Review not found</h1>"

        delete_query = "DELETE FROM reviews WHERE id = ?"
        cursor.execute(delete_query, (review_id, ))

        # Update overall ratings once review is deleted
        ratings_query = "SELECT rating FROM reviews WHERE book_id = ?"
        ratings = cursor.execute(ratings_query, (book_id,)).fetchall()
        ratings = [rating[0] for rating in ratings]

        overall_ratings = sum(ratings)/len(ratings)
        if overall_ratings.is_integer():
            overall_ratings = int(overall_ratings)
        else:
            overall_ratings = "%.1f" % overall_ratings

        overall_ratings_query = "UPDATE books SET rating = ? WHERE id = ?"
        cursor.execute(overall_ratings_query, (overall_ratings, book_id))

        conn.commit()
        conn.close()

        if request.headers.get('Accept') == 'application/json':
            return jsonify({"message": f"Deleted a review for {book_info[0]} by {book_info[1]}"})
        else:
            return f"Deleted a review for {book_info[0]} by {book_info[1]}"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

@app.route('/books/<int:book_id>', methods = ['GET', 'DELETE'])
def delete_one_book(book_id):
    try:
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
    except Exception as error:
        print(f"Error connecting to books database: {error}")

    try:
        book_query = "SELECT title, author FROM books WHERE id = ?"
        book_info = cursor.execute(book_query, (book_id,)).fetchone()

        if book_info is None:
            if request.headers.get('Accept') == 'application/json':
                conn.close()
                return jsonify({"Error": "Book not found"}), 404
            else:
                conn.close()
                return "<h1>404 Error: Book not found</h1>"

        delete_reviews = "DELETE FROM reviews WHERE book_id = ?"
        cursor.execute(delete_reviews, (book_id, ))

        delete_query = "DELETE FROM books WHERE id = ?"
        cursor.execute(delete_query, (book_id, ))

        conn.commit()
        conn.close()
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"message": f"Deleted {book_info[0]} by {book_info[1]} from Book Club"})
        else:
            return f"Deleted {book_info[0]} by {book_info[1]} from Book Club"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")
@app.route('/books/delete_all', methods = ['GET', 'DELETE']) 
def delete_all_books():
    try:
        conn = sqlite3.connect('books.db')
    except Exception as error:
        print(f"Error connecting to books database: {error}")
    try:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reviews")
        cursor.execute("DELETE FROM books")
        conn.commit()
        conn.close()

        if request.headers.get('Accept') == 'application/json':
            return jsonify({"message": "All books deleted from your Book Club"})
        else:
            return "All books deleted from your Book Club"
    except Exception as error:
        conn.close()
        try:
            if request.headers.get('Accept') == 'application/json':
                return jsonify({"Error": "An internal error occurred"}), 500
            else:
                return "<h1>500 Error: An internal error occurred</h1>"
        except Exception:
            print(f"Error: {error}")

if __name__ == '__main__':
    if os.getenv("PORT") is None:
        app.run(debug=True)
    else:
        app.run(debug=True, port=int(os.getenv("PORT")))
