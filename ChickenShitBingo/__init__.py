from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '6c5ff70ab1a65ef44bf936b08062589f'

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:goforit@localhost/chickenShitBingo'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hgyhbtmcjbmsaw:5545399e3523f7caafd6e6ed10ede332eefd74369eba6e8bf62b502affcad569@ec2-3-231-16-122.compute-1.amazonaws.com:5432/dcf5v10tbuk6li'
    db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_HOST_USER')  #os.environ.get('CHICKENSHITBINGO_EMAIL_HOST') 
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_HOST_PASSWORD')

mail = Mail(app)

from ChickenShitBingo import routes














# import os
# from flask import Flask, render_template, request,url_for, flash, redirect 
# from datetime import datetime
# from flask_login import UserMixin, login_user, current_user, logout_user, login_required
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail 

# app = Flask(__name__)



# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# mail = Mail(app)
# app.config['SECRET_KEY'] = '6c5ff70ab1a65ef44bf936b08062589f'

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'norely.flask.blog@gmail.com'
# app.config['MAIL_PASSWORD'] = 'qzjs1trav*'

# # you also need to change ENV in models.py
# ENV = 'dev'


# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:goforit@localhost/chickenShitBingo'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hgyhbtmcjbmsaw:5545399e3523f7caafd6e6ed10ede332eefd74369eba6e8bf62b502affcad569@ec2-3-231-16-122.compute-1.amazonaws.com:5432/dcf5v10tbuk6li'
#     db = SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# db = SQLAlchemy(app)

# from flaskblog.users.routes import users
# from flaskblog.main.routes import main

# app.register_blueprint(users)
# app.register_blueprint(main)


# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
    
# # from flask import render_template, url_for, flash, redirect, request, Blueprint
# # from flask_login import login_user, current_user, logout_user, login_required
# # from flaskblog import db, bcrypt
# # from flaskblog.models import User, Post
# # from flaskblog.users.forms import (RegistrationForm, LogInForm, UpdateAccountForm,
# #                                    RequestResetForm, ResetPasswordForm)
# # from flaskblog.users.utils import save_picture, send_reset_email

# # users = Blueprint('users', __name__)


# @app.route("/register",methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     if form.validate_on_submit():
#         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Account created for {form.username.data}!','success')
#         return redirect(url_for('users.login'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/login",methods=['GET','POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = LogInForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('main.home'))
#         else:
#             flash('Login unsuccessful. Please check your email and password','danger')
#     return render_template('login.html', title='Log In', form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('main.home'))


# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)


# @app.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def request_reset():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('request_reset.html', title='Reset Password', form=form)


# @app.route("/reset_password/<token>", methods=['GET','POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('The password reset has expired, or is from an invalid email.', 'warning')
#         return redirect(url_for('users.reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_pw
#         db.session.commit()
#         flash(f'Your password has been updated!','success')
#         return redirect(url_for('users.login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)