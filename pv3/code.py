from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "paishfgos9823a.j23.s"
db = SQLAlchemy(app)

class Asiakkaat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String, nullable=False)
	lastname= db.Column(db.String, nullable=False)
	number = db.Column(db.String, nullable=False)

AsiakkaatForm = model_form(Asiakkaat, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def base():
	db.create_all()

	asiakkaat = Asiakkaat(firstname="Krister", lastname="Karlsson", number="1234456")
	db.session.add(asiakkaat)

	asiakkaat = Asiakkaat(firstname="Erkki", lastname="Esimerkki", number="987665")
	db.session.add(asiakkaat)

	db.session.commit()

@app.route("/")
def index():
	asiakkaat = Asiakkaat.query.all()
	return render_template("index.html", asiakkaat=asiakkaat)

@app.route("/data", methods=["GET", "POST"])
def data():
	form = AsiakkaatForm()
	print(request.form)
	return render_template("data.html", form=form)

app.run()
