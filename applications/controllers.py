from flask import Flask, render_template, request, url_for, redirect, session
from flask import current_app as app
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, FormField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from applications.models import *
from applications.forms import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"


@login_manager.user_loader
def load_user(username):
    return Userinfo.query.get(username)


@app.route('/signin', methods=['GET', 'POST'])
def signin():  # put application's code here
    form = signinForm()
    print(form.validate_on_submit(), "================================================================================================")
    if form.validate_on_submit():
        print("hi")
        userinfo = Userinfo.query.filter_by(username=form.username.data).first()
        print(userinfo)
        if userinfo:
            if userinfo.password == form.password.data:
                return redirect(url_for('profile'))
    return render_template('signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # put application's code here
    form = signupForm()
    if form.validate_on_submit():
        new_user = Userinfo(username=form.username.data,f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():  # put application's code here'
    return render_template("profile.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():  # put application's code here'
    logout_user()
    return redirect(url_for('signin'))
