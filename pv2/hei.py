from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("base.html", name="Coder")

@app.route("/loop")
def loop():
	animals = ["lion", "tiger", "rabbit", "racoon"]
	return render_template("loop.html", name="Krister", animals=animals)

@app.route("/post", methods=["GET", "POST"])
def post():
        return render_template("post.html", name="Visitor")

@app.route("/get", methods=["GET", "POST"])
def get():
        return render_template("get.html", name="Visitor")

@app.route("/date", methods=["GET", "POST"])
def date():
        return render_template("date.html", name="Visitor")


app.run()
