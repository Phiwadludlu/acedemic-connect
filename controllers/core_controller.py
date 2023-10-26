
"""The controllers module is for business logic"""
from flask import request, render_template, flash, redirect, url_for, session, jsonify
from flask_security import hash_password, anonymous_user_required, auth_required
from flask_security.decorators import roles_required

from forms.auth_forms.sign_up_form import StudentRegisterForm, LecturerRegisterForm
from models import Student, User, Role, db, Lecturer, Appointment, Module, TimeSlot, RescheduledApproval
from utils.enums import ApprovalStatusChoices, AttendanceChoices
from utils.create_db_tables import  create_tables
from flask_login import current_user
from services import api_service as api_s
from services.populate_moduletable import run as populate_module_run
from sqlalchemy import and_
import uuid
import json
from datetime import datetime

@anonymous_user_required
def index():
    return render_template("views/LandingpageView.html")

def create_db_tables():

        create_tables()
        return "Done"

def populate_tables():
    populate_module_run()
    return "All done!"


@anonymous_user_required
def signUp():
    return redirect(url_for('core_routes.student_sign_up'))


@anonymous_user_required
def lecturer_sign_up():
    register_lecturer_form = LecturerRegisterForm()

    if request.method == "POST":
        if register_lecturer_form.validate_on_submit():
            lecturer_role = Role.query.filter_by(id=3).first_or_404()

            # Add user to DB logic here
            new_user = User(email=register_lecturer_form.email.data,
                            password=hash_password(register_lecturer_form.password.data), active=True)
            new_user.fs_uniquifier = new_user.get_auth_token()
            new_user.is_active = True
            new_user.roles.append(lecturer_role)

            new_lecturer = Lecturer(staff_number=register_lecturer_form.staff_number.data, user=new_user)

            db.session.add(new_user)
            db.session.add(new_lecturer)
            db.session.commit()

            flash("Account created successfully", category="info")

            return redirect(url_for("security.login"))

    return render_template("components/forms/auth_forms/lecturer_form.html",
                           register_lecturer_form=register_lecturer_form)


@anonymous_user_required
def student_sign_up():
    register_student_form = StudentRegisterForm()

    if request.method == "POST":
        if register_student_form.validate_on_submit():
            student_role = Role.query.filter_by(id=2).first_or_404()

            # Add user to DB logic here
            new_user = User(email=register_student_form.email.data,
                            password=hash_password(register_student_form.password.data), active=True)
            new_user.fs_uniquifier = new_user.get_auth_token()
            new_user.is_active = True
            new_user.roles.append(student_role)

            new_student = Student(student_number=register_student_form.student_number.data, user=new_user)
            new_student.student_firstname = register_student_form.first_name.data
            new_student.student_lastname = register_student_form.last_name.data
            new_student.create_full_name()

            db.session.add(new_user)
            db.session.add(new_student)
            db.session.commit()

            flash("Account created successfully", category="info")

            return redirect(url_for("security.login"))

    return render_template("components/forms/auth_forms/student_form.html", register_student_form=register_student_form)


@auth_required()
def proxy_redirect():
    user_id = session["_user_id"]
    current_user = User.query.filter_by(fs_uniquifier=user_id).first()

    if current_user.has_role('student'):

        return redirect(url_for("student_route.index"))

    elif current_user.has_role('lecturer'):

        return redirect(url_for("lecturer_route.index"))

@auth_required()
def calendar():
    #Reschudule approval
    return render_template("views/Calendar.html")

@auth_required()
def notifications():
    #Notifications
    return render_template("views/Notifications.html")

@auth_required()
def single_appointment(appointment_uuid):
    # TODO: Determine the view to render based on appointment details
    #       If approval_status == Reschedule, show reschedule view
    #       else show appointment details as normal

    appointment = db.session.query(Appointment).filter( Appointment.appointment_uuid == appointment_uuid).first()
    old_timeslot = None
    if appointment.is_reschedule:
        old_appointment_id = RescheduledApproval.query.filter(RescheduledApproval.new_appointment_id == appointment.id).first()
        old_appointment = Appointment.query.filter(Appointment.id == old_appointment_id.id).first()
        old_timeslot = TimeSlot.query.filter(TimeSlot.id == old_appointment.timeslot_id).first()
    
    module = db.session.query(Module).filter( Module.id == appointment.module_id).first()
    student = db.session.query(Student).filter( Student.id == appointment.student_id).first()
    timeslot = db.session.query(TimeSlot).filter( TimeSlot.id == appointment.timeslot_id).first()
    appointment_collection = (appointment, module, student, timeslot, old_timeslot)
    
    appointment_data = api_s.format_single_appointment_data(appointment_collection)
    return render_template("views/Appointment.html", appointment=appointment_data, current_user=current_user)

@roles_required('lecturer')
def reschedule_appointment(appointment_uuid):
    if request.method == "GET":
        appointment = db.session.query(Appointment, Module, Student, TimeSlot, None).filter(and_(Appointment.module_id == Module.id, Student.id == Appointment.student_id, Appointment.timeslot_id == TimeSlot.id, Appointment.appointment_uuid == appointment_uuid)).first()
        return render_template("views/RescheduleAppointment.html", appointment=api_s.format_single_appointment_data(appointment))
    if request.method == "POST":
        try:
            appointment_record = Appointment.query.filter(Appointment.appointment_uuid == appointment_uuid).first()
            timeslot = TimeSlot.query.filter(TimeSlot.id == appointment_record.timeslot_id).first()
            
            appointment_record.approval_status = ApprovalStatusChoices.RESCHEDULED
            appointment_record.attendance_status = AttendanceChoices.RESCHEDULED
            timeslot.is_available = True

            db.session.add(timeslot)
            db.session.add(appointment_record)
            db.session.flush()

            req_data = request.data
            form_data = json.loads(req_data)

            appointment_reason = form_data["appointment_reason"]
            appointment_date = form_data["appointment_date"]
            appointment_timeslot = form_data["appointment_timeslot_id"]
            appointment_uuid = str(uuid.uuid1())


            new_appointment = Appointment(date=datetime.fromisoformat(appointment_date),approval_status=ApprovalStatusChoices.PENDING,attendance_status=AttendanceChoices.PENDING,  appointment_reason="[RESCHEDULED] \n %s" % (appointment_reason),appointment_uuid=appointment_uuid,    lecturer_id=appointment_record.lecturer_id, student_id=appointment_record.student_id,   timeslot_id=appointment_timeslot,module_id=appointment_record.module_id, is_reschedule=True)
            db.session.add(new_appointment)
            db.session.flush()

            reschedule_approval_appointment=RescheduledApproval(old_appointment_id=appointment_record.id,new_appointment_id=new_appointment.id)
            db.session.add(reschedule_approval_appointment)
            db.session.commit()

            return jsonify({"code" : 1})
        except:
            return jsonify({"code" : -1})

@auth_required()
def approve_appointment(appointment_uuid):
    appointment = Appointment.query.filter(Appointment.appointment_uuid == appointment_uuid).first()
    appointment.approval_status = ApprovalStatusChoices.APPROVED
    db.session.add(appointment)
    db.session.flush()

    all_pending_appointments_with_same_timeslot = Appointment.query.filter(and_(Appointment.timeslot_id == appointment.timeslot_id,Appointment.id != appointment.id)).all()

    for record in all_pending_appointments_with_same_timeslot:
        record.approval_status = ApprovalStatusChoices.DECLINED
        record.attendance_status = AttendanceChoices.DECLINED
        db.session.add(record)

    db.session.commit()

    return redirect('/appointment/%s' % (appointment_uuid))

@auth_required()
def decline_appointment(appointment_uuid):
    appointment = Appointment.query.filter(Appointment.appointment_uuid == appointment_uuid).first()
    appointment.approval_status = ApprovalStatusChoices.DECLINED
    appointment.attendance_status = AttendanceChoices.DECLINED
    
    timeslot = TimeSlot.query.filter(TimeSlot.id == appointment.timeslot_id).first()
    timeslot.is_available = True

    db.session.add(timeslot)
    db.session.add(appointment)
    db.session.commit()

    return redirect('/appointment/%s' % (appointment_uuid))

def not_found(error):
   return render_template("views/404.html"), 404