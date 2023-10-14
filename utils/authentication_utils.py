from models.auth_models.user_model import User
from wtforms import (EmailField, StringField, IntegerField, PasswordField, validators)


def student_number_validator(form, field):
    """Checks if theres no user with a similar student number"""

    user = User.query.filter_by(email=field.data).first()

    if user:
        raise validators.ValidationError('Student Number is already in use')


def staff_number_validator(form, field):
    "Checks if a staff number already exists"

    pass

