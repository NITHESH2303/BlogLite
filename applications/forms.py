from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Length

from applications.models import *


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