from flask import request, redirect, render_template
from controllers import api_controller as api_ctrl
from services import api_service as api_s
from models import Appointment, RescheduledApproval
from utils.enums import ApprovalStatusChoices, AttendanceChoices
from sqlalchemy import and_, or_
from flask_login import current_user
from flask_security.decorators import roles_required


@roles_required('student')
def index():
    #Student Dashboard
    tag = request.args.get('tag')
    upcoming_appointments = api_ctrl.fetch_student_appointments().filter(and_(Appointment.approval_status == ApprovalStatusChoices.APPROVED, Appointment.attendance_status == AttendanceChoices.PENDING)).order_by(Appointment.date.asc()).all()
    old_appointments = api_ctrl.fetch_student_appointments().filter(and_( or_(Appointment.approval_status == ApprovalStatusChoices.APPROVED, Appointment.approval_status == ApprovalStatusChoices.DECLINED, Appointment.approval_status == ApprovalStatusChoices.RESCHEDULED), Appointment.attendance_status != AttendanceChoices.PENDING)).order_by(Appointment.date.desc()).all()
    pending_appointments = api_ctrl.fetch_student_appointments().filter(Appointment.approval_status == ApprovalStatusChoices.PENDING).order_by(Appointment.date.asc()).all()
    if tag==None:
        return render_template("views/student/partial/Upcoming.html", upcoming_appointments=api_s.format_appointments_tile_data(upcoming_appointments))
    elif tag.lower() == "upcoming":
        return render_template("views/student/partial/Upcoming.html", upcoming_appointments=api_s.format_appointments_tile_data(upcoming_appointments))
    elif tag.lower() == "history":
        return render_template("views/student/partial/History.html", old_appointments=api_s.format_appointments_tile_data(old_appointments))
    elif tag.lower() == "pending":
        return render_template("views/student/partial/Pending.html", pending_appointments=api_s.format_appointments_tile_data(pending_appointments))
    else:
        return redirect('/student?tag=Upcoming')
    
@roles_required('student')
def book_appointment():
    #Booking an appointment
    return render_template("views/student/BookAppointment.html", current_user=current_user)

