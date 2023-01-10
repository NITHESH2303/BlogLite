from datetime import datetime

from flask import render_template, url_for, redirect, session, current_app, request, flash
from flask import current_app as app
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from flask_session import Session
from sqlalchemy import exc

from applications.forms import *
from applications.models import *

Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


@login_manager.user_loader
def load_user(id):
    return Userinfo.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def signin():  # put application's code here
    form = signinForm()
    # if request.method == 'GET':
    #     session['login'] = False
    #     return render_template('signin.html', form=form)
    # else:
    if form.validate_on_submit():
        user = db.session.query(Userinfo).filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                # user.last_login = str(datetime.today())[:16]
                login_user(user)
                return redirect(url_for('profile', username=user.username))
    return render_template('signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # put application's code here
    form = signupForm()
    if form.validate_on_submit():
        new_user = Userinfo(username=form.username.data, f_name=form.f_name.data, l_name=form.l_name.data,
                            email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):  # put application's code here'
    # username = db.session.query(Userinfo).filter(Userinfo.username == username).first()
    return render_template("profile.html", username=username)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():  # put application's code here'
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('signin'))

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():  # put application's code here'
#     form = UploadForm()
#     if form.validate_on_submit():
#         filename = photos.save(form.photo.data)
#         return render_template('upload.html', filename=filename)
