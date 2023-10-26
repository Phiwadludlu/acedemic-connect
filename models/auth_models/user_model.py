from models import db
from datetime import datetime
from flask_security.models import fsqla_v3 as fsqla
from .roles_model import RoleUsers, Role
from sqlalchemy.orm import relationship, backref


# USER MODEL


class User(db.Model, fsqla.FsUserMixin):
    """Stores user information such as email username and password"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    # is_student = db.Column(db.Boolean, nullable=False, default=False)
    # is_lecturer = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # One to one relationship with student table

    student = db.relationship('Student', uselist=False, back_populates='user')

    # One to one relationship with student table

    lecturer = db.relationship('Lecturer', uselist=False, back_populates='user')

    # Relationship with the roles table
    roles = db.relationship('Role', secondary='roles_users', backref=backref("users", lazy="dynamic"))

    notifications = db.relationship("Notification", back_populates="user")



