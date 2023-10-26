import datetime

from models import db
from utils.enums import ApprovalStatusChoices,AttendanceChoices

class Appointment(db.Model):

    __tablename__ = "appointment"

    id = db.Column(db.Integer(),primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    approval_status = db.Column(db.Enum(ApprovalStatusChoices))
    attendance_status = db.Column(db.Enum(AttendanceChoices))
    appointment_reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    appointment_uuid = db.Column(db.String(255))
    is_reschedule = db.Column(db.Boolean(), default=False)

    lecturer_id = db.Column(db.Integer(),db.ForeignKey("lecturers.id"))
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"))
    timeslot_id = db.Column(db.Integer(), db.ForeignKey("timeslot.id"))
    module_id = db.Column(db.Integer(), db.ForeignKey("modules.id"))



    #Relationship with lecturer

    lecturer = db.relationship("Lecturer", back_populates="appointment")

    #Relationship with student

    student = db.relationship("Student", back_populates="appointment")

    #Relationship with timeslot

    timeslot = db.relationship("TimeSlot", back_populates="appointment")