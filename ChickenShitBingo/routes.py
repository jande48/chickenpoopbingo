from flask import render_template, url_for, flash, redirect, request, jsonify
from ChickenShitBingo import app, db, bcrypt, mail
from ChickenShitBingo.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from ChickenShitBingo.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json

# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]

# @app.route("/getCredits", methods=['GET'])
# def getCredits():
#     if current_user.is_authenticated:
#             res = current_user.credits
#             print(res)
#             return res

        #print(card["1"])
        #title = req_data['title']
        #body = req_data['body']
        # clicked=request.get_json(silent=True)
        # title = request.form.get('title')
        # body = request.form.get('body')
        # flash('it worked!!!', 'success')
        #return '<div class="alert alert-success" role="alert">Your Card Has Been Saved</div>'
    # return render_template('home.html')

@app.route("/saveCard", methods=['GET','POST'])
def saveCard():
    # clicked = None
    if request.method == "POST":
        if current_user.is_authenticated:
            req_data = request.form['myData']
            #print(req_data)
            card = json.loads(req_data)
            minusCreditsNew = 0
            for i in range(25):
                if card[str(i)]==1:
                    minusCreditsNew+=1
            previousCard = json.loads(current_user.card)
            minusCreditsOld = 0
            for i in range(25):
                if previousCard[str(i)]==1:
                    minusCreditsOld+=1
            
            current_user.credits = str(int(current_user.credits)-(minusCreditsNew-minusCreditsOld))
            current_user.card = req_data
            #print(current_user.card)
            #print(type(current_user.card))
            db.session.commit()
        else:
            flash('Please Sign In to Save a Card!', 'info')
    
    if request.method == "GET":
        if current_user.is_authenticated:
            res = current_user.credits
            return res
        #print(card["1"])
        #title = req_data['title']
        #body = req_data['body']
        # clicked=request.get_json(silent=True)
        # title = request.form.get('title')
        # body = request.form.get('body')
        # flash('it worked!!!', 'success')
        #return '<div class="alert alert-success" role="alert">Your Card Has Been Saved</div>'
    return render_template('home.html')

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    # if current_user.is_authenticated:
    #     minus_credits = 0
    #     # for i in range( len(current_user.card.data) ):
    #     #     minus_credits += int(current_user.card.data[i])
    #     # current_user.credits.data = int(current_user.credits.data)-minus_credits
    #     # db.session.commit()
    #     # flash('Your Card Has Been Saved! Tune in For the Next Chicken Shitting.', 'success')
    # else:
    #     flash('Please Sign In to Save a Card!', 'info')
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)