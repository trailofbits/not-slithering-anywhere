from app import app, db, models
from flask import (render_template_string, request, render_template,
                   redirect, session)
import uuid


@app.route("/")
def index():
    if 'authd' not in session:
        return redirect('/login')

    returnUrl = request.args.get('returnURL') or None
    message = request.args.get('message') or None

    if message is not None:
        return render_template_string(message)

    return render_template("main.html")


@app.route("/posts/add", methods=["GET", "POST"])
def posts_add():
    if 'authd' not in session:
        return redirect('/login')

    # if you wanted to talk sensitive data protection
    # within logs, I think this would be an interesting
    # location, so I'll accept posts via both GET and 
    # POST here. GET is almost certainly wrong if you
    # consider user data sensitive, ignoring the fact
    # that it *also* is incorrect as per RFC-2616

    if request.method == "POST":
        post_text = request.form.get("post")
    else:
        post_text = request.query.get("post")

    user = models.Person.query.filter_by(username=session["username"]).first()
    pid = str(uuid.uuid4())
    post = models.Post(post=post_text, postid=pid, userid=user.id)
    db.session.add(post)
    db.session.commit()

    return redirect('/posts')


@app.route("/posts")
def posts():

    search = request.args.get('search') or None

    posts = None

    if search is not None:
        posts = models.Post.filter(models.Post.post.contains(search))
    else:
        posts = models.Post.query.all()

    return render_template('posts.html',
                           posts=posts,
                           search=search)


@app.route("/posts/<person>")
def posts_person(person):
    if 'authd' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route("/friends")
def friends():
    if 'authd' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route("/friends/add/<person>")
def friend_add(person):
    if 'authd' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route("/friends/unfriend/<person>")
def friend_remove(person):
    if 'authd' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        userid = uuid.uuid4()
        user = models.Person(username=username, userid=str(userid))
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['authd'] = True
        return redirect('/posts')
    else:
        if 'authd' in session:
            return redirect('/posts')

        return render_template('register.html',
                               message=request.form.get("message"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        user = models.Person.query.filter_by(username=username).first()

        if user is None:
            return redirect('/login?message="no such user"')

        session['username'] = username
        session['authd'] = True
        return redirect('/posts')

    else:
        if 'authd' in session:
            return redirect('/posts')

        return render_template('register.html',
                               login=True,
                               message=request.form.get("message"))


@app.route("/logout")
def logout():
    if 'username' in session:
        del(session['username'])
    if 'authd' in session:
        del(session['authd'])
    return redirect('/login')
