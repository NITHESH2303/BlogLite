from flask import render_template, url_for, redirect
from flask import current_app as app
from applications.forms import *
from applications.models import *


@app.route('/login', methods=['GET', 'POST'])
def signin():  # put application's code here
    form = signinForm()
    if form.validate_on_submit():
        user = Userinfo.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('profile'))
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


@app.route('/profile', methods=['GET', 'POST'])
def profile():  # put application's code here'
    return render_template("profile.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():  # put application's code here'
    return redirect(url_for('signin'))
