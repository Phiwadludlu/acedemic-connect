from models import db

class RescheduledApproval(db.Model):

    __tablename__ = "rescheduled_approval"

    id = db.Column(db.Integer(), primary_key =True)
    old_appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id", name="old_appointment_id"))
    new_appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id", name ="new_appointment_id"))
    reason_for_reschedule = db.Column(db.String(255))