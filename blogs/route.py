from flask import render_template, request, redirect, jsonify, flash,url_for
from flask_mysqldb import MySQL 
from blogs.form import RegistrationForm, LoginForm
from blogs import app, bcrypt , login_user, current_user, logout_user, login_required, User, Post



@app.route('/')
def home():
    return render_template("home.html",title='Trang chủ')

@app.route('/about')
def about():
    return render_template("about.html",title='Trang chủ')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account create for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("register.html",title='Đăng ký',form=form)
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and  bcrypt.check_password_hash(user.password,form.password.data):
            flash(f'Đã đăng nhập {form.username.data}!','success') 
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Đã đăng nhập không thành công vui lòng kiểm tra lại!','danger') 
    return render_template("login.html",title='Đăng nhập',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route('/account')
@login_required
def account():
    logout_user()
    return render_template("account.html",title='Tài khoản')