from flask import render_template, url_for, redirect, session, current_app, request, flash, jsonify, g
from flask import current_app as app
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from flask_uploads import UploadSet, IMAGES

from applications.forms import *
from applications.models import *

photos = UploadSet('photos', IMAGES)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def signin():  # put application's code here
    form = signinForm()
    # if request.method == 'GET':
    #     session['login'] = False
    #     return render_template('signin.html', form=form)
    # else:
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
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
        new_user = User(username=form.username.data, f_name=form.f_name.data, l_name=form.l_name.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):  # put application's code here'
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)

    count = 0

    # if request.method == 'POST' and 'photo' in request.files:
    #     filename = photos.save(request.files['photo'])
    #     url = photos.url(filename)
    #     ui = url.replace('_uploads', 'static')
    #     desc = request.form['desc']
    #     post = Post(img=ui, author=current_user, description=desc)
    #     db.session.add(post)
    #     db.session.commit()
    #     return redirect('/profile/<username>')
    return render_template("profile.html", username=username, user=user, posts=posts, count=count)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():  # put application's code here'
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('signin'))


@app.route('/addpost', methods=['GET', 'POST'])
def upload():  # put application's code here'
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        url = photos.url(filename)
        ui = url.replace('_uploads', 'static')
        desc = request.form['desc']
        post = Post(img=ui, author=current_user, description=desc)
        db.session.add(post)
        db.session.commit()
    return render_template('addpost.html')

