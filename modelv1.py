from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email,EqualTo
from flask_login import UserMixin,AnonymousUserMixin


db = SQLAlchemy()

class auth(db.Model,UserMixin,AnonymousUserMixin):
    __tablename__ = 'auth'
    auth_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.auth_id)  # Return a string representation of the user ID

    @property
    def is_authenticated(self):
        return True  # You can customize this based on your application logic

    @property
    def is_anonymous(self):
        return True

    def __init__(self, email, password):
        self.email = email
        self.password = password

class SignupForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[
      DataRequired(),EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Signup')

    def validate_user(self, email):
        existing_user = auth.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
