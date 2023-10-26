from models import Student,Lecturer
from wtforms import (EmailField, StringField, IntegerField, PasswordField, validators)


def student_number_validator(form, field):
    """Checks if theres no user with a similar student number"""

    student = Student.query.filter_by(student_number = field.data).first()

    if student != None:
        raise validators.ValidationError('Student Number is already in use')


def staff_number_validator(form, field):
    "Checks if a staff number already exists"

    lecturer = Lecturer.query.filter_by(staff_number = field.data).first()

    if lecturer !=None:
        raise validators.ValidationError('Staff Number already in use')

