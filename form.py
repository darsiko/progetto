from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=150)])
    address = StringField('address', validators=[DataRequired(), Length(min=2, max=150)])
    role = SelectField('role', choices=[('buyer', 'buyer'), ('seller', 'seller')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')
