from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, Length
from flask_login import current_user
from malay.models import User

class SigninForm(FlaskForm):
    username = StringField('Enter Your Username', validators=[DataRequired('You must Enter a Username')])
    password = PasswordField('Enter Password', validators=[DataRequired('Field should not be empty')])

    def validate_login(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValueError('Something is wrong')
               
    

class SignupForm(FlaskForm):
    username = StringField(
        'Enter Your Username', validators=[DataRequired('You must Enter a Username'),
        Length(min=5,max=20, message='Username must not exceed 5 to 20 characters'),
        Regexp('^[A-Za-z0-9_]{3,}$', message='Username can only contain letters, numbers and underscore')
    ])
    email = StringField('Enter Your Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Enter Password', validators=[
        DataRequired('Field should not be empty'), EqualTo('password2', 'Password does not match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired('Field should not be empty')])

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValueError('Username has been taken')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValueError('Email has been taken')

class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Enter Your Username', validators=[
        Length(min=5,max=20, message='Username must not exceed 5 to 20 characters'),
        Regexp('^[A-Za-z0-9_]{3,}$', message='Username can only contain letters, numbers and underscore')
    ])
    email = StringField('Enter Your Email', validators=[Email()])
    accountBalance = StringField('Account Balance')
    pendingBalance = StringField('Pending Balance')
    amountOnHold = StringField('Amount on Hold')
    billing = IntegerField('Enter your client billing, omope')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValueError('Username has been taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValueError('Email has been taken')
    
class ChangePassword(FlaskForm):
    password1 = StringField('New Password', validators=[
        EqualTo('password2', 'Password does not match')])
    password2 = StringField('Confirm New Password', validators=[])