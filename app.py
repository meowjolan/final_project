# -*- coding: UTF-8 -*-

from Form import LoginForm, RegisterForm, ArticleForm, CommentForm
from Database import Database

import os

from flask import Flask, request, sessions, redirect, url_for, render_template, send_from_directory
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user


app = Flask(__name__)
app.secret_key = 'secret key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username, password, introduction):
        self.id = id
        self.username = username
        self.password = password
        self.introduction = introduction

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.id, self.username, self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    db = Database()
    return db.get_user_info_by_id(id)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 在不要求登录的页面先进行注销
    logout_user()

    loginForm = LoginForm()
    message = False
    if request.method == 'POST' and loginForm.validate_on_submit():
        db = Database()
        result = db.validate_login(request.form['username'], request.form['password'])
        if result:
            # print(user_id)
            user = User(result[0], result[1], result[2], result[3])
            login_user(user)
            return redirect(url_for('home', user_id=user.id))
        else:
            message = "Incorrect username or password!"
    return render_template('login.html', loginform=loginForm, message=message, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 在不要求登录的页面先进行注销
    logout_user()

    registerForm = RegisterForm()
    message = False
    if request.method == 'POST' and registerForm.validate_on_submit():
        db = Database()
        result = db.check_if_username_exist(request.form['username'])
        if result:
            message = "Username already exists!"
        else:
            db.add_user(request.form['username'], request.form['password'])
            return redirect(url_for('login'))

    return render_template('register.html', registerform=registerForm,
                           message=message, current_user=current_user)


@login_manager.user_loader
def load_user(id):
    db = Database()
    result = db.get_user_by_id(id)
    if type(result) == tuple:
        return User(result[0], result[1], result[2], result[3])


@app.route('/home?user_id=<user_id>')
@login_required
def home(user_id):
    db = Database()
    _, username, _, description = db.get_user_by_id(user_id)
    friends = db.get_friends_info_by_id(user_id)
    return render_template('home.html', current_user=current_user,
                           username=username, description=description, friends=friends)


@app.route('/home')
@login_required
def homepage():
    return redirect(url_for('home', user_id=current_user.id))


@app.route('/article')
@login_required
def article():
    return redirect(url_for('article_user', user_id=current_user.id))


@app.route('/article_edit', methods=['POST', 'GET'])
@login_required
def article_edit():
    articleForm = ArticleForm()
    if request.method == 'POST' and articleForm.validate_on_submit():
        db = Database()
        article_id = db.add_article(request.form['title'],
                                    request.form['text'],
                                    request.form['authority'])
        db.add_user_article_id(article_id, current_user.id)
        # 处理tag
        tags = request.values.getlist('tags')
        tags = list(set(tags))
        for tag_name in tags:
            tag_id = db.add_tag(tag_name)
            db.add_tag_article_id(article_id, tag_id)

        return redirect(url_for('article'))

    return render_template('article_edit.html', articleform=articleForm, current_user=current_user)


@app.route('/article?article_id=<article_id>', methods=['POST', 'GET'])
@login_required
def article_detail(article_id):
    commentForm = CommentForm()
    db = Database()
    article = db.get_article_by_id(article_id)
    tags = db.get_tag_name_by_article_id(article_id)
    comments = db.get_comment_by_article_id(article_id)

    if request.method == 'POST' and commentForm.validate_on_submit():
        com_id = db.add_comment(request.form['text'])
        db.add_comment_user_id(com_id, current_user.id)
        db.add_article_comment_id(com_id, article_id)

        return redirect(url_for('article_detail', article_id=article_id))

    return render_template('article_detail.html', article=article,
                           tags=tags, comments=comments, commentform=commentForm,
                           current_user=current_user)


@app.route('/article?user_id=<user_id>')
@login_required
def article_user(user_id):
    db = Database()
    articles = db.get_article_by_user_id(user_id)
    tags = [db.get_tag_name_by_article_id(article_id)
            for article_id, _, _, _, _ in articles]

    collections = []
    if user_id == current_user.id:
        for i in range(len(articles)):
            collections.append([a for a in articles[i]] + [tags[i]])
    else:
        for i in range(len(articles)):
            if int(articles[i][4]) == 1:
                collections.append([a for a in articles[i]] + [tags[i]])

    return render_template('article.html', collections=collections,
                           current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)