from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "maijiloapsao1sha3Ux33th"
db = SQLAlchemy(app)

class Students(db.Model):
	ID = db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String, nullable=False)
	Studentnmbr = db.Column(db.String, nullable=False)
	Address = db.Column(db.String, nullable=False)

StudentsForm = model_form(Students, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def database():
	db.create_all()

	students = Students(Name="Krister", Studentnmbr="1234898", Address="Helsinki 6 B")
	db.session.add(students)

	students = Students(Name="Maija", Studentnmbr="9994898", Address="Turku 17 A")
	db.session.add(students)

	db.session.commit()

@app.route("/")
def laksy():
	students = Students.query.all()
	return render_template("laksy.html", students=students)

app.run()

