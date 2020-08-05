from app import app, db, models, PostBackup
from flask import (render_template_string, request, render_template,
                   redirect, session, send_file)
from functools import wraps
import uuid
import re
import io
import pickle


uid_re = re.compile("[a-zA-Z0-9\-]*")


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'authd' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    if 'authd' not in session:
        return redirect('/login')

    returnUrl = request.args.get('returnURL') or None
    message = request.args.get('message') or None

    if message is not None:
        return render_template_string(message)

    if returnUrl is not None:
        return redirect(returnUrl)

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
        post_text = request.args.get("post")

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


@app.route("/posts/backup")
def posts_backup():

    if 'authd' not  in session:
        return redirect('/login')

    posts = models.Post.query.all()
    post_backup = PostBackup(posts)
    fh = io.BytesIO()
    pickle.dump(post_backup, fh)
    fh.seek(0)
    return send_file(fh,
                     as_attachment=True,
                     attachment_filename="Backup.pickle")


@app.route("/posts/backup_verify", methods=["GET", "POST"])
def posts_backup_verify():

    if 'authd' not in session:
        return redirect('/login')


    if request.method == 'POST':
        if 'backup' not in request.files:
            return render_template('upload.html',
                                   message='file not uploaded')

        fh = request.files['backup']
        try:
            posts = pickle.load(fh)
            return render_template('upload.html',
                                   message="upload verified successfully")
        except Exception as e:
            return render_template('upload.html',
                                   message=e)
    else:
        return render_template('upload.html')


@app.route("/posts/<person>")
def posts_person(person):
    if 'authd' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route('/people')
def people():

    query_prefix = "SELECT * FROM person WHERE username like '%"

    if 'authd' not in session:
        return redirect('/login')

    if "search" in request.args:
        search = request.args.get("search")
        people = db.session.execute(query_prefix + search + "%'")
        return render_template("people_search.html",
                               people=people,
                               search=search)
    else:
        return render_template("people_search.html")


@app.route('/people/<uid>')
@auth_required
def people_by_id(uid):

    query = "SELECT * FROM person WHERE userid = :userid"

    res = uid_re.search(uid)

    people = None

    if res.end() == 0:
        people = []
    else:
        people = db.session.execute(query, {"userid":uid})

    return render_template("people_search.html",
                           people=people)


@app.route("/friends")
def friends():
    if 'auth' not in session:
        return redirect('/login')
    return "<h1>Working</h1>"


@app.route("/friends/add/<person>")
def friend_add(person):
    if 'authd' in session:
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
                               message=request.args.get("message"))


@app.route("/logout")
def logout():
    if 'username' in session:
        del(session['username'])
    if 'authd' in session:
        del(session['authd'])

    if 'message' in request.args:
        return render_template_string(request.args.get("message"))

    return redirect('/login')
