from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo
import database_mangement as db_manger


class registerUserForm(FlaskForm):
    username = StringField(label="Enter Your Username:", validators=[DataRequired(), Length(max=40)])
    password = PasswordField(label="Enter a Password:", validators=[DataRequired(), Length(max=40)], id='password')
    confirm_pw = PasswordField(label="Confirm your Password:",
                               validators=[DataRequired(message='*Required'),
                                           EqualTo('password', message='Both password fields must be equal!'),
                                           Length(max=40)])
    toggle_pw = BooleanField(label="Show Password", id='check')
    first_name = StringField(label="Enter your First Name:", validators=[DataRequired(), Length(max=30)])
    last_name = StringField(label="Enter your Last Name:", validators=[DataRequired(), Length(max=30)])
    gender = SelectField(label="Select your Gender:", choices=["Male", "Female", "Other"])
    dob = DateField(label="Enter your Date of Birth:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

    def validate_username(self, username):
        user = db_manger.get_unique_user(username=username.data)
        if len(user) != 0:
            raise ValidationError("User Already Exists!")