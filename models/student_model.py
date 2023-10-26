from models import db
from datetime import datetime
from .auth_models.user_model import User
from sqlalchemy.orm import backref, relationship

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer(), primary_key=True)
    student_number = db.Column(db.String(255), unique=True)
    student_firstname =  db.Column(db.String(255))
    student_lastname = db.Column(db.String(255))
    student_fullname =  db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



    #Relationship with User model
    user = db.relationship("User", back_populates="student")

    #Relationship with appointment

    appointment = db.relationship("Appointment", back_populates="student")

    #Relationship with qualification

    qualifications = relationship('Qualification', secondary='qualification_period',
                                  backref=backref('students', lazy="dynamic"))


    def create_full_name(self):

        self.student_fullname = self.student_firstname +" "+ self.student_lastname