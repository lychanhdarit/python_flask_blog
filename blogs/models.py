from blogs import db, login_manager, 
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    username = db.Column(db.String(200),unique=True,nullable=False)
    email = db.Column(db.String(200),unique=True,nullable=False)
    image_file = db.Column(db.String(200),unique=True,nullable=False,default='noimg.jpg')
    password = db.Column(db.String(200),unique=True,nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, 
                                    default = datetime.utcnow) 
    image_file = db.Column(db.String(200),unique=True,nullable=False)
    content = db.Column(db.String(2000),unique=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.name}','{self.date_posted}')"