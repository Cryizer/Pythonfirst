from flask import Flask, render_template, flash, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key = "Ieph1che9Ea3Phighul5FohM0iivee"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///kk'
db = SQLAlchemy(app)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	desc = db.Column(db.Text(160), nullable=False)

BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)

	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])

## User utility functions

def currentUser():
	try:
		uid = int(session["uid"])
	except:
		return None
	return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

def loginRequired():
	if not currentUser():
		abort(403)

## User view

@app.route("/user/login", methods=["GET", "POST"])
def loginView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data

		password = form.password.data


		user = User.query.filter_by(email=email).first()
		if not user:
			flash("Login failed.")
			print("No such user")
			return redirect("/user/login")
		if not user.checkPassword(password):
			flash("Login failed.")
			print("Wrong password")
			return redirect("/user/login")

		session["uid"]=user.id

		flash("Login successful.")
		return redirect("/")

	return render_template("login.html", form=form)

@app.route("/user/register", methods=["GET", "POST"])
def registerView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data

		password = form.password.data


		if User.query.filter_by(email=email).first():
			flash("User already exits! Please log in.")
			return redirect("/user/login")

		user = User(email=email)
		user.setPassword(password)

		db.session.add(user)
		db.session.commit()

		flash("Registration successfull. Welcome! Now, log in.")
		return redirect("/user/login")

	return render_template("register.html", form=form)

@app.route("/user/logout")
def logoutView():
	session["uid"] = None
	flash("Logged out. See you again!")
	return redirect("/")

## Main views

@app.before_first_request
def initDb():
	db.create_all()


@app.errorhandler(404)
def custom404(e):
	return render_template("404.html")

@app.route("/book/<int:id>/edit", methods=["GET", "POST"])
@app.route("/book/add", methods=["GET", "POST"])
def addView(id=None):
	loginRequired()
	book = Book()
	if id:
		book = Book.query.get_or_404(id)

	fields = BookForm(obj=book)

	if fields.validate_on_submit():
		fields.populate_obj(book)
		db.session.add(book)
		db.session.commit()

		flash("Added!")
		return redirect("/")

	return render_template("add.html", fields=fields)

@app.route("/book/<int:id>/delete")
def deleteView(id):
	loginRequired()
	book = Book.query.get_or_404(id)
	db.session.delete(book)
	db.session.commit()

	flash("Deleted.")
	return redirect("/")

@app.route("/")
def indexView():
	books = Book.query.all()
	return render_template("index.html", books=books)
