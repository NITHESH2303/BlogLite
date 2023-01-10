from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
# from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, ValidationError, Length

from applications.models import *

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class signupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    f_name = StringField('First Name', validators=[InputRequired()])
    l_name = StringField('Last Name')
    email = StringField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Signup')

    def validate_username(self, username):
        existing_username = Userinfo.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError('Username already exists')


class signinForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=100)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

# class UploadForm(FlaskForm):
#     photo = FileField('Photo', validators=[
#         FileAllowed(photos, 'Only images are allowed'),
#         FileRequired('File should not be empty')
#     ])
#     submit = SubmitField('Upload')
