from models import db

class QualificationPeriod(db.Model):

    __tablename__ = "qualification_period"

    id = db.Column(db.Integer(), primary_key =True)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"))
    qualification_id = db.Column(db.Integer(), db.ForeignKey("qualification.id"))
    start_year = db.Column(db.String(4))
    end_year = db.Column(db.String(4))