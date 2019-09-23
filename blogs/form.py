from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blogs import User
from flask_login import current_user
class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=2,max=50)])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password  = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        #Kiểm tra user
        users = User.query.filter_by(username = username.data).first()# lấy dữ liệu
        if users:
            raise ValidationError('Username đã tồn tại chon username khác')
    def validate_email(self,email):
            #Kiểm tra user
        users = User.query.filter_by(email = email.data).first()# lấy dữ liệu
        if users:
            raise ValidationError('Email đã tồn tại')  

class AccountForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=2,max=50)])
    submit = SubmitField('Update')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(min=2,max=50)])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()]) 
    picture = FileField('Update profile picture', validators =[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField('Update') 
    def validate_username(self,username):
         #Kiểm tra user
        if username.data != current_user.username: 
            users = User.query.filter_by(username = username.data).first()# lấy dữ liệu
            if users:
                raise ValidationError('Username đã tồn tại chon username khác')
    def validate_email(self,email):
         #Kiểm tra user
        if email.data != current_user.email: 
            users = User.query.filter_by(email = email.data).first()# lấy dữ liệu
            if users:
                raise ValidationError('Email đã tồn tại')  

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password  = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreatePostForm(FlaskForm):
    name = StringField('Tieu de',validators=[DataRequired()])
    content = TextAreaField('Noi dung',validators=[DataRequired()])
    #date_posted = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update picture', validators =[FileAllowed(['jpg','png','jpeg','gif'])])
    #user_id = 
    submit = SubmitField('Post') 