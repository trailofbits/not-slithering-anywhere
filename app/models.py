from app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    userid = db.Column(db.Text)

    def __repr__(self):
        return "Person<username: {0}, userid: {1}>".format(self.username,
                                                           self.userid)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text)
    postid = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('person.id'))
