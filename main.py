from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

"""Using SQLAlchemy to Create a Database and Table"""


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<User {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        all_books = Book.query.all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        book_in_database = db.get_or_404(Book, request.args.get('id'))
        return render_template("edit.html", book=book_in_database)

    elif request.method == "POST":
        book_in_database = db.get_or_404(Book, request.form["id"])
        book_in_database.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/delete", methods=["GET"])
def delete():
    book_in_database = db.get_or_404(Book, request.args.get('id'))
    db.session.delete(book_in_database)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
