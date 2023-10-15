from models import  db
from sqlalchemy.orm import Relationship, backref

class Module(db.Model):
    __tablename__ ="modules"

    id = db.Column(db.Integer(), primary_key =True)
    name = db.Column(db.String())
    code = db.Column (db.String(), unique=True)
    lecturer_id = db.Column(db.Integer(), db.ForeignKey("lecturers.id"))

    #Relationship with lecturer

    lecturer = db.relationship("Lecturer", back_populates="module")