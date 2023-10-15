from models import  db
from utils.enums import DayChoices

class TimeSlot(db.Model):

    __tablename__ = "timeslot"

    id = db.Column(db.Integer(), primary_key =True)
    day = db.Column(db.Enum(DayChoices))
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    lecturer_id = db.Column(db.Integer(), db.ForeignKey("lecturers.id"))

    #Relationship with lecturer

    lecturer = db.relationship("Lecturer", back_populates="timeslot")

    #Relattionship with appointment

    appointment = db.relationship("Appointment", back_populates="timeslot")