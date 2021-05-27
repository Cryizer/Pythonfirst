from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "ikoeQueGhaisushohShoreiphein5e"
db = SQLAlchemy(app)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String, nullable=False)
	lastname = db.Column(db.String, nullable=False)
	address = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	phone = db.Column(db.String, nullable=False)

BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def Dbase():
	db.create_all()

@app.route("/")
def index():
	books = Book.query.all()
	return render_template("addressbook.html", books=books)

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/add", methods=["GET", "POST"])
def add(id=None):
	book = Book()
	if id:
		book = Book.query.get_or_404(id)

	form = BookForm(obj=book)

	if form.validate_on_submit():
		form.populate_obj(book)

		db.session.add(book)
		db.session.commit()

		flash("Register updated")
		return redirect("/")
	return render_template("addaddress.html", form=form)

@app.route("/<int:id>/delete")
def deletepage(id):
	book = Book.query.get_or_404(id)
	db.session.delete(book)
	db.session.commit()

	flash("Deleted.")
	return redirect("/")

if __name__ == "__main__":
        app.run()

