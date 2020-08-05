from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ast

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)


class PostBackup(object):
    def __init__(self, posts):
        self.posts  = {}

        if type(posts) is dict:
            self.posts = posts
        else:
            for  post in posts:
                self.posts[post.postid] = dict(userid=post.userid,
                                               post=post)

    def  __reduce__(self):
        return (self.__class__,(self.posts,))


from app import routes, models
