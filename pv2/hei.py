from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def index():
	animals = ["lion", "tiger", "rabbit", "racoon"]
	return render_template("base.html", name="Krister",  animals=animals)

@app.route("/kek")
def kek():
        return render_template("kek.html", name="Krister")

app.run()
