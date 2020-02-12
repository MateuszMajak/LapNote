from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from CircuitsTimes.models import Users, Cars, Tracks, LapTimes


# class ScrapForm(FlaskForm):
#     scrap = SubmitField('Scrap')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    YearOfBirth = IntegerField('Year of birth',
                               validators=[DataRequired(), NumberRange(min=1880, max=2020)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        mail = Users.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    CarID = IntegerField('You can save the ID of your Car here :)')
    private = IntegerField('Change privacy settings (0 - Public, 1 - Private)', validators=[NumberRange(min=0, max=1)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class AddTimeForm(FlaskForm):
    track = IntegerField('ID of the Track',
                         validators=[DataRequired()])
    car = IntegerField('ID of the Car')
    comment = StringField('Comment', validators=[Length(max=100)])
    time = FloatField('Type your time in seconds', validators=[DataRequired()])
    submit = SubmitField('Add')
