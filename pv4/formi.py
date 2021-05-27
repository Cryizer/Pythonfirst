from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app= Flask(__name__)
app.secret_key = "jakIOam83maohyaC411KFiI"
db  = SQLAlchemy(app)

class Food(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

FoodForm = model_form(Food, base_class=FlaskForm, db_session=db.session)

class Bug(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	color = db.Column(db.String, nullable=False)

BugForm = model_form(Bug, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def Dbase():
	db.create_all()

	food = Food(name="Strawberry milkshake")
	db.session.add(food)

	food = Food(name="Pizza")
	db.session.add(food)

	food = Food(name="Roasted ants")
	db.session.add(food)

	bug = Bug(name="Ant", color="Black")
	db.session.add(bug)

	db.session.commit()

@app.route("/")
def index():
	foods = Food.query.all()
	return render_template("index.html", foods=foods)


@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/add", methods=["GET", "POST"])
def add(id=None):
	food = Food()
	if id:
		food = Food.query.get_or_404(id)

	form = FoodForm(obj=food)

	if form.validate_on_submit():
		form.populate_obj(food)

		db.session.add(food)
		db.session.commit()

		flash("Added your food")
		return redirect("/")
	return render_template("add.html", form=form)


@app.route("/bug")
def bugdb():
        bugs = Bug.query.all()
        return render_template("bug.html", bugs=bugs)


@app.route("/bug/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def editing(id=None):
        bug = Bug()
        if id:
                bug = Bug.query.get_or_404(id)

        form = BugForm(obj=bug)

        if form.validate_on_submit():
                form.populate_obj(bug)

                db.session.add(bug)
                db.session.commit()

                flash("Added bug you saw")
                return redirect("/bug")
        return render_template("saw.html", form=form)


if __name__ == "__main__":
	app.run()
