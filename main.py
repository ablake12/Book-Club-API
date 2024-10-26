from flask import Flask, render_template, jsonify, request#import flask libraries
import os
import sqlite3

app = Flask(__name__)#create Flask object

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
            current_book TEXT NOT NULL DEFAULT 'N'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            review TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

@app.route('/books/', methods = ['GET']) 
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    books = cursor.execute("SELECT * FROM books").fetchall()
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
                json_response["reviews"] = reviews  
            else:
                json_response["reviews"] = []
            final_json_response.append(json_response)

        conn.close()
        return jsonify(final_json_response)
    else:
        conn.close()
        return render_template('bookUI.html', books=books, review_counts=review_counts)

@app.route('/books/read', methods = ['GET']) 
def get_read_books():
    conn = sqlite3.connect('books.db')
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

@app.route('/books/unread', methods = ['GET']) 
def get_unread_books():
    conn = sqlite3.connect('books.db')
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

@app.route('/books/current', methods = ['GET']) 
def get_current_book():
    conn = sqlite3.connect('books.db')
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

@app.route('/books/reviews/<int:book_id>')
def get_reviews(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    book_query = "SELECT title, author, id FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()
    review_query = "SELECT * FROM reviews WHERE book_id = ?"
    reviews = cursor.execute(review_query, (book_id,)).fetchall()
    conn.close()

    if request.headers.get('Accept') == 'application/json':
        final_json_response = []
        for review in reviews:
            review_response = {}
            review_response["id"] = review[0]
            review_response["book_id"] = review[1]
            review_response["review"] = review[2]
            final_json_response.append(review_response)
        
        return jsonify({"title": book_info[0], "author": book_info[1], "reviews": final_json_response})
    else:
        return render_template('reviewUI.html', book_info=book_info, reviews=reviews)

@app.route('/add_book')  # Route to render the form
def book_form():
    return render_template('addBookUI.html')

@app.route('/add_book', methods = ['POST']) 
def add_book():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    if request.is_json:
        json_form = request.get_json()
        title = json_form.get("title")
        author = json_form.get("author")
        genre = json_form.get("genre")
        desc = json_form.get("description")
        is_read = json_form.get("read_status")
        current_book = json_form.get("current_status")
    else:
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        desc = request.form.get("description")
        is_read = request.form.get("read_status")
        current_book = request.form.get("current_status")

    if is_read is None:
        if current_book is None:
            book_query = f"INSERT INTO books (title, author, genre, description) VALUES (?, ?, ?, ?)"
            cursor.execute(book_query, (title, author, genre, desc))
        else:
            if current_book.upper() in ('Y', 'N'):
                # add logic for updating any current books to N if the value is Y
                if current_book.upper() == 'Y':
                    cursor.execute(f"UPDATE books SET current_book = 'N' WHERE current_book = 'Y'") # Update the current book to not being read
                book_query = f"INSERT INTO books (title, author, genre, description, current_book) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(book_query, (title, author, genre, desc, current_book))
            else:
                return jsonify({"ValueError": "current_book is not 'Y' or 'N'"})
    else:
        if is_read.upper() in ('Y', 'N'):
            if current_book is None:
                book_query = f"INSERT INTO books (title, author, genre, description, is_read) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(book_query, (title, author, genre, desc, is_read))
            else:
                if current_book.upper() in ('Y', 'N'):
                    # add logic for updating any current books to N if the value is Y
                    if current_book.upper() == 'Y':
                        cursor.execute(f"UPDATE books SET current_book = 'N' WHERE current_book = 'Y'") # Update the current book to not being read
                    book_query = f"INSERT INTO books (title, author, genre, description, is_read, current_book) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(book_query, (title, author, genre, desc, is_read, current_book))
                else:
                    return jsonify({"ValueError": "current_book is not 'Y' or 'N'"})
        else:
            return jsonify({"ValueError": "read_status is not 'Y' or 'N'"})
            
    conn.commit()
    conn.close()
    if request.is_json:
        return jsonify({"message": f"{title} by {author} added to the Book Club"})
    else:
        return f"{title} by {author} added to the Book Club"
    
@app.route('/books/<int:book_id>/add_reviews')  # Route to render the form
def review_form(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    conn.close()

    return render_template('addReviewUI.html', book_info=book_info, book_id=book_id)

@app.route('/books/<int:book_id>/add_reviews', methods = ['POST']) 
def add_review(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    if request.is_json:
        json_form = request.get_json()
        review = json_form.get("review")
    else:
        review = request.form["review"]

    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    review_query = f"INSERT INTO reviews (book_id, review) VALUES (?, ?)"
    cursor.execute(review_query, (book_id, review))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({"message": f"Review added for {book_info[0]} by {book_info[1]}"})
    else:
        return f"Review added for {book_info[0]} by {book_info[1]}"

@app.route('/books/<int:book_id>/reviews/<int:review_id>')
def update_review_form(book_id, review_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    conn.close()

    return render_template('updateReviewUI.html', book_info=book_info, book_id=book_id, review_id=review_id)

@app.route('/books/<int:book_id>/reviews/<int:review_id>', methods = ['POST', 'PUT']) 
def update_review(book_id, review_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    if request.is_json:
        json_form = request.get_json()
        review = json_form.get("review")
    else:
        review = request.form["review"]
    
    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    review_query = f"UPDATE reviews SET review = ? WHERE id = ?"
    cursor.execute(review_query, (review, review_id))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({"message": f"Review {review_id} updated for {book_info[0]} by {book_info[1]}"})
    else:
        return f"Review {review_id} updated for {book_info[0]} by {book_info[1]}"


@app.route('/books/<int:book_id>/status', methods = ['GET', 'PUT']) 
def update_read_status(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    book_query = "SELECT title, author, is_read FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

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

    if request.is_json:
        return jsonify({"message": return_msg})
    else:
        return return_msg


@app.route('/books/<int:book_id>/current', methods = ['GET', 'PUT']) 
def update_current_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    # First update the existing current book to N
    cursor.execute("UPDATE books SET current_book = 'N' WHERE current_book = 'Y'")

    # Then update the current book with the id
    update_query = f"UPDATE books SET current_book = 'Y' WHERE id = ?"
    cursor.execute(update_query, (book_id, ))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({"message": f"{book_info[0]} by {book_info[1]} updated to the club's current book"})
    else:
        return f"{book_info[0]} by {book_info[1]} updated to the club's current book"

@app.route('/books/<int:book_id>/reviews/<int:review_id>', methods = ['GET', 'DELETE']) 
def delete_review(book_id, review_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    review_check_query = "SELECT * FROM reviews WHERE book_id = ? AND id = ?"
    review_check = cursor.execute(review_check_query, (book_id, review_id)).fetchone()
    if review_check is None:
        conn.close()
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": "Review not found"}), 404
        else:
            return "404 error: Review not found"

    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

    delete_query = "DELETE FROM books WHERE id = ?"
    cursor.execute(delete_query, (book_id, ))

    conn.commit()
    conn.close()

    if request.headers.get('Accept') == 'application/json':
        return jsonify({"message": f"Deleted a review for {book_info[0]} by {book_info[1]}"})
    else:
        return f"Deleted a review for {book_info[0]} by {book_info[1]}"
@app.route('/books/<int:book_id>', methods = ['GET', 'DELETE'])
def delete_one_book(book_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    book_check_query = "SELECT * FROM books WHERE id = ?"
    book_check = cursor.execute(book_check_query, (book_id, )).fetchone()
    if book_check is None:
        conn.close()
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": "Book not found"}), 404
        else:
            return "404 error: Book not found"

    book_query = "SELECT title, author FROM books WHERE id = ?"
    book_info = cursor.execute(book_query, (book_id,)).fetchone()

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

@app.route('/books/delete_all', methods = ['GET', 'DELETE']) 
def delete_all_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reviews")
    cursor.execute("DELETE FROM books")
    conn.commit()
    conn.close()

    if request.headers.get('Accept') == 'application/json':
        return jsonify({"message": "All books deleted from your Book Club"})
    else:
        return "All books deleted from your Book Club"

if __name__ == '__main__':
    if os.getenv("PORT") is None:
        app.run(debug=True)
    else:
        app.run(debug=True, port=int(os.getenv("PORT")))
