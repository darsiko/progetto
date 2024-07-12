from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, NumberRange


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


class AddProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=150)])
    description = StringField('description', validators=[DataRequired(), Length(min=10, max=1000)])
    amount = IntegerField('amount', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField('category', choices=[('Electronics', 'Electronics'), ('Clothing', 'Clothing'),
                                                ('Home and kitchen', 'Home and kitchen'), ('Books', 'Books'),
                                                ('Health and beauty', 'Health and beauty'), ('Toys', 'Toys'),
                                                ('Sport and free time', 'Sport and free time'),
                                                ('Car and motorcycle', 'Car and motorcycle')],
                           validators=[DataRequired()])
    file = FileField('file', validators=[FileRequired(), FileAllowed(['jpg'])])
    submit = SubmitField('Add')


class ModifyUser(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', validators=[DataRequired(), Length(min=2, max=150)])
    role = SelectField('role', choices=[('buyer', 'buyer'), ('seller', 'seller'), ('admin', 'admin')],
                       validators=[DataRequired()])
    submit = SubmitField('Edit')


class ReviewForm(FlaskForm):
    score = DecimalField('score', validators=[DataRequired(),
                                              NumberRange(min=1, max=5, message="Score must be between 1 and 5")])
    text = StringField('description', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit')
