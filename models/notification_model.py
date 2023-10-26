
from models import db
from datetime import datetime
from .auth_models.user_model import User
from sqlalchemy.orm import backref, relationship
from utils.enums import NotificationStatus

class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(db.Integer(), primary_key=True)
    action = db.Column(db.String())
    message = db.Column(db.String())
    status = db.Column(db.Enum(NotificationStatus))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


    user = db.relationship("User", back_populates="notifications")