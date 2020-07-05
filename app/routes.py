from app import app
from flask import render_template_string, request


@app.route("/")
def index():
    returnUrl = request.args.get('returnURL') or None
    message = request.args.get('message') or None

    if message is not None:
        return render_template_string(message)

    return "<h1>Working</h1>"


@app.route("/posts/add")
def posts_add():
    return "<h1>Working</h1>"


@app.route("/posts")
def posts():

    search = request.args.get('search') or None

    if search is not None:
        pass

    return "<h1>Working</h1>"


@app.route("/posts/<person>")
def posts_person(person):
    return "<h1>Working</h1>"


@app.route("/friends")
def friends():
    return "<h1>Working</h1>"


@app.route("/friends/add/<person>")
def friend_add(person):
    return "<h1>Working</h1>"


@app.route("/friends/unfriend/<person>")
def friend_remove(person):
    return "<h1>Working</h1>"


@app.route("/register")
def register():
    return "<h1>Working</h1>"


@app.route("/login")
def login():
    return "<h1>Working</h1>"


@app.route("/logout")
def logout():
    return "<h1>Working</h1>"
