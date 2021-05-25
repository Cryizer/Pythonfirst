from flask import Flask, render_template

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("base.html", name="Krister")

@app.route("/kek")
def kek():
	animals = ["lion", "tiger", "rabbit", "racoon"]
	return render_template("kek.html", name="Krister", animals=animals)

@app.route("/foo", methods=["GET", "POST"])
def foo():
        return render_template("foo.html", name="Krister")

@app.route("/get", methods=["GET", "POST"])
def get():
        return render_template("get.html", name="Krister")


app.run()
