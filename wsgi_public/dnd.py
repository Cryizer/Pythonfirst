from flask import Flask, render_template, flash, redirect, session, abort, jsonify, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators
import random
import re

app = Flask(__name__)
app.secret_key = "Ieph1che9Ea3Phighul5FohMshfjtyre"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///kkwsgi'
db = SQLAlchemy(app)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	role = db.Column(db.String, nullable=False)
	desc = db.Column(db.Text(160), nullable=False)


PlayerForm = model_form(Player, base_class=FlaskForm, db_session=db.session)


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	category = db.Column(db.String, nullable=False)
	desc = db.Column(db.Text(160), nullable=False)

ItemForm = model_form(Item, base_class=FlaskForm, db_session=db.session)

class Anon(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)

	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)

class AnonForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])

## User utility functions

def currentUser():
	try:
		uid = int(session["uid"])
	except:
		return None
	return Anon.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

def loginRequired():
	if not currentUser():
		abort(403)

## User view

@app.route("/user/login", methods=["GET", "POST"])
def loginView():
	form = AnonForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data


		anon = Anon.query.filter_by(email=email).first()
		if not anon:
			flash("Login failed.")
			print("No such user")
			return redirect("/user/login")
		if not anon.checkPassword(password):
			flash("Login failed.")
			print("Wrong password")
			return redirect("/user/login")

		session["uid"]=anon.id

		flash("Login successful.")
		return redirect("/")

	return render_template("login.html", form=form)

@app.route("/user/register", methods=["GET", "POST"])
def registerView():
	form = AnonForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data


		if Anon.query.filter_by(email=email).first():
			flash("User already exits! Please log in.")
			return redirect("/user/login")

		anon = Anon(email=email)
		anon.setPassword(password)

		db.session.add(anon)
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

@app.route("/player/<int:id>/edit", methods=["GET", "POST"])
@app.route("/player/add", methods=["GET", "POST"])
def addView(id=None):
	loginRequired()
	player = Player()
	if id:
		player = Player.query.get_or_404(id)

	fields = PlayerForm(obj=player)

	if fields.validate_on_submit():
		fields.populate_obj(player)
		db.session.add(player)
		db.session.commit()

		flash("Added!")
		return redirect("/")

	return render_template("add.html", fields=fields)

@app.route("/player/<int:id>/delete")
def deleteView(id):
	loginRequired()
	player = Player.query.get_or_404(id)
	db.session.delete(player)
	db.session.commit()

	flash("Deleted.")
	return redirect("/")

@app.route("/")
def indexView():
	players = Player.query.all()
	return render_template("index.html", players=players)

@app.route("/items/<int:id>/edit", methods=["GET", "POST"])
@app.route("/items/add", methods=["GET", "POST"])
def addItem(id=None):
        loginRequired()
        item = Item()
        if id:
                item = Item.query.get_or_404(id)

        fields = ItemForm(obj=item)

        if fields.validate_on_submit():
                fields.populate_obj(item)
                db.session.add(item)
                db.session.commit()

                flash("Added!")
                return redirect("/items")

        return render_template("additem.html", fields=fields)

@app.route("/items/<int:id>/delete")
def deleteItem(id):
        loginRequired()
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()

        flash("Deleted.")
        return redirect("/items")

@app.route("/items")
def itemView():
        items = Item.query.all()
        return render_template("item.html", items=items)

dice_page = """
<!doctype html>
<html lang=en>
        <head>
                <title>Dice roller</title>
                <meta charset="utf-8">
        </head>
        <body>
                <nav>
	                        <a href="/">Home</a> -
                                <a href="/player/add">Add player profile</a> -
                                <a href="/items">Item database</a> -
                                <a href="/items/add">Add Items</a> -
                                <a href="/dice">Roll dice</a> -
                                <a href="/user/logout">Logout</a> 
                </nav>

                <h1>Dice Roller</h1> <br>
		<p>Choose the number of dice and dice type to throw</p> <br>
                <form method="POST" action="/dice">
                        <label for="diceString">Dice:</label>
                        <input type="text" id="diceString" name="diceString" placeholder="1d20">
                        <input type="submit" value="Submit"><br><br>
                        <label>Query:</label><br><br>
            <label>Result:</label>
                </form>
        </body>
</html>
"""

dice_page2 = re.sub("(Query:)", "\\1 {{ query }}", dice_page)
dice_page2 = re.sub("(Result:)", "\\1 {{ result }} {{ rolls }}", dice_page2)

@app.route("/dice", methods=["GET"])
def index():
        return dice_page

@app.route("/dice", methods=["GET", "POST"])
def diceRoller():
	if request.method == "POST":
		text = request.form.get("diceString").replace(" ", "")
		die = re.findall("(?:(\d+)d(\d+))", text)
		if die == []:
			die = [("", 1, 20)]
		user_rolls = roll(int(die[0][0]), int(die[0][1]))
		reroll = re.findall("r([ro])(\d+)", text)
		if reroll != [] and int(reroll[0][1]) <= int(die[0][1]) and int(die[0][1]) != 1:
			if reroll[0][0] == "o":
				instances_of_number = [i for i, val in enumerate(user_rolls["list"]) if val == int(reroll[0][1])]
				instances_offset = 0
				for each_instance in instances_of_number:
					user_rolls["list"][each_instance+instances_offset] = reroll[0][1] + " (rerolled)"
					instances_offset +=1
					user_rolls["list"].insert(each_instance+instances_offset, roll(1, int(die[0][1]))["sum"])
				user_rolls["sum"] = sum([i if type(i) == int else 0 for i in user_rolls["list"]])
			else:
				while int(reroll[0][1]) in user_rolls["list"]:
					instances_of_number = [i for i, val in enumerate(user_rolls["list"]) if val == int(reroll[0][1])]
					instances_offset = 0
					for each_instance in instances_of_number:
						user_rolls["list"][each_instance+instances_offset] = reroll[0][1] + " (rerolled)"
						instances_offset +=1
						user_rolls["list"].insert(each_instance+instances_offset, roll(1, int(die[0][1]))["sum"])
				user_rolls["sum"] = sum([i if type(i) == int else 0 for i in user_rolls["list"]])
		keep = re.findall("k([hl])(\d+)", text)
		if keep != [] and int(keep[0][1]) < int(die[0][1]):
			keep_list = [i for i in user_rolls["list"] if type(i) == int]
			keep_list.sort()
			if keep[0][0] == "h":
				keep_list = keep_list[len(keep_list)-int(keep[0][1]):]
			else:
				keep_list = keep_list[:int(keep[0][1])]
			user_rolls["sum"] = str(sum(keep_list)) + " " + str(keep_list) + " ||"
	templateData = {"query": text, "result": user_rolls["sum"], "rolls": user_rolls["list"]}
	return render_template_string(dice_page2, **templateData)

def roll(num, sides):
	rolls = [random.randint(1, sides) for i in range(num)]
	roll_sum = sum(rolls)
	return({"list": rolls, "sum": roll_sum})
