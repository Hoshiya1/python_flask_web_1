from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.urls import url_parse
from app.models import User, Post
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
# 这样，必须登录后才能访问首页了,会自动跳转至登录页
@login_required
def index():
    
    
    # posts = db.session.query(Post).all()
    posts = Post.query.all()
    return render_template('index.html', user=current_user, posts=posts)

@app.route('/login', methods=['POST', 'GET'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        #根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        #判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            #然后重定向到登录页面
            return redirect(url_for('login'))
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user,remember=form.remember_me.data)
        #此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        #如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        #综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    #首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title='登录', form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    # 如果手动输入的不是当前用户名，返回首页
    if current_user.username != username:
        return redirect(url_for('index'))

    form = PostForm()
    if form.body.data != None:
        current_user.posts.append(Post(body=form.body.data, timestamp=datetime.now()))
        db.session.add(current_user)
        db.session.commit()
        form.body.data = None
    
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title=user.username, user=user, posts=user.posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑', form=form)