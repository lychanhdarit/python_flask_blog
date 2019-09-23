from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import yaml


app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'b92aea7c8651242a00793d6fa1a98197'
bcrypt = Bcrypt(app)
#Đăng ký login_manager
login_manager = LoginManager(app)
#Thiết lập trang yêu cầu login
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#File yaml chưa các thông tin cấu hình 
dbConfig = yaml.load(open('db.yaml'))
#Cấu hình kết nối database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+dbConfig['mysql_user']+':'+dbConfig['mysql_password'] +'@'+dbConfig['mysql_host']+'/'+dbConfig['mysql_db']
db = SQLAlchemy(app)

from datetime import datetime 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    username = db.Column(db.String(200),unique=True,nullable=False)
    email = db.Column(db.String(200),unique=True,nullable=False)
    image_file = db.Column(db.String(200),nullable=False,default='noimg.jpg')
    password = db.Column(db.String(200),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)
    is_active = db.Column(db.Boolean,default= True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, 
                                    default = datetime.utcnow) 
    image_file = db.Column(db.String(200),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.name}','{self.date_posted}')"


from blogs import route