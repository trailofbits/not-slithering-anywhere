from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    userid = db.Column(db.Text)

    def __repr__(self):
        return "Person<username: %s, userid: %s>".format(self.username,
                                                         self.userid)
