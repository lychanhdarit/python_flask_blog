import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, jsonify, flash,url_for, request, abort
from blogs.form import RegistrationForm, LoginForm, UpdateAccountForm, CreatePostForm
from blogs import db, app, bcrypt , login_user, current_user, logout_user, login_required, User, Post
from datetime import datetime 


@app.route('/') 
@app.route('/news')
def home():
    page = request.args.get('page',1,type=int)
    #posts = Post.query.all()
    #dir(posts) / posts.per_page / posts.page / posts.total
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=1,page=page)
    return render_template("home.html",title='Trang chủ',posts=posts)

@app.route('/about')
def about():
    return render_template("about.html",title='Trang chủ')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_2 = User(username=form.username.data,image_file = secrets.token_hex(8),email=form.email.data,name=form.name.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user_2)
        db.session.commit()
        flash(f'Account create for {form.username.data}!','success')
        return redirect(url_for('login'))
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
            #next_page trang yau cau login
            next_page = request.args.get('next')
            #Tra ve trang yeu cau login
            return  redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Đã đăng nhập không thành công vui lòng kiểm tra lại!','danger') 
    return render_template("login.html",title='Đăng nhập',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/images',picture_fn)
    
    #output_size = (125,125)
    #i = Image.open(form_picture)
    #i.thumbnail(output_size)
    #i.save(picture_path)
    form_picture.save(picture_path)
    return picture_fn
@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    image_file = url_for('static',filename='images/'+current_user.image_file)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        
        db.session.commit()
        flash(f'Account update success!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name 
    return render_template("account.html",title='account',form=form,image_file=image_file) 

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post(): 
    form = CreatePostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) 
        post = Post(name=form.name.data,content=form.content.data,date_posted = datetime.utcnow(), user_id = current_user.id,image_file = picture_file)
        db.session.add(post)
        db.session.commit()
        flash(f'Dang thanh cong','success')
        return redirect(url_for('home'))
        
    return render_template("new_post.html",title='New post',form=form)
@app.route('/post/<int:post_id>') 
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",title=post.name,post=post) 

@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.user_id != current_user.id):
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        post.name = form.name.data
        post.content = form.content.data  
        db.session.commit()
        flash(f'Post update success!','success')
        return redirect(url_for('post',post_id= post.id))
    elif request.method == 'GET':
        form.name.data = post.name
        form.content.data = post.content 
    return render_template("update_post.html",title=post.name,form=form) 

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.user_id != current_user.id):
        abort(403)
    db.session.delete(post) 
    db.session.commit() 
    flash(f'Post Delete success!','success')
    return redirect(url_for('home'))  