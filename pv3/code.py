from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Asiakkaat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String, nullable=False)
	lastname= db.Column(db.String, nullable=False)
	number = db.Column(db.String, nullable=False)

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

app.run()
