from flask import g
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError



class confirmIdentity(FlaskForm):
    password = PasswordField(label="Confirm Your Password:", validators=[DataRequired(), Length(max=40)], id='password')
    toggle_pw = BooleanField(label="Show Password", id='check')
    submit = SubmitField(label="Submit")

    def validate_password(self, password):
        if g.user[2] != password.data:
            raise ValidationError("Password Incorrect, Try Again")
