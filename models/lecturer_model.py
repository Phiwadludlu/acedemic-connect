from models import db
from datetime import datetime

from sqlalchemy.types import DateTime
from .auth_models.user_model import User


class Lecturer(db.Model):

    __tablename__ = "lecturers"

    id = db.Column(db.Integer(), primary_key=True)
    staff_number = db.Column(db.String(255), unique=True)
    modified_at = db.Column(db.DateTime(), default=datetime.now)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    # Define the back-reference to User
    user = db.relationship('User', back_populates='lecturer')

