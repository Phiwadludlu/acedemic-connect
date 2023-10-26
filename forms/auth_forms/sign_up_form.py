from flask_security.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, PasswordField, StringField,
                     validators)

from models.auth_models.user_model import User
from utils.authentication_utils import student_number_validator, staff_number_validator


class StudentSignUp(FlaskForm):

    first_name = StringField("First Name", validators=[validators.DataRequired()])
    last_name = StringField("Last Name", validators=[validators.DataRequired()])
    email = EmailField("Email", validators=[validators.Email(), validators.DataRequired()])
    student_number = IntegerField("Student Number", validators=[validators.DataRequired(),
                                                                validators.length(min=8, max=8,
                                                                                  message="Student number is invalid")])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[validators.DataRequired()])


class LecturerSignUp(FlaskForm):
    email = EmailField("Email", validators=[validators.Email(), validators.DataRequired()])
    staff_number = IntegerField("Staff Number",
                                validators=[validators.Length(min=8, max=10, message="Invalid staff number"),
                                            validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    confirm_password = PasswordField("Confrim password", validators=[validators.DataRequired()])


class StudentRegisterForm(RegisterForm):
    first_name = StringField("First Name", validators=[validators.DataRequired()])
    last_name = StringField("Last Name", validators=[validators.DataRequired()])
    student_number = StringField("Student Number", validators=[validators.DataRequired(),
                                                               validators.length(min=8, max=8,
                                                                                 message="Student number is invalid"),
                                                               student_number_validator])


class LecturerRegisterForm(RegisterForm):
    staff_number = StringField("Staff Number", validators=[validators.DataRequired(), validators.length(min=8, max=8,
                                                                                                        message="Student number is invalid"),
                                                           staff_number_validator])
