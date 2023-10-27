from flask import request, redirect, render_template, url_for
from controllers import api_controller as api_ctrl
from services import api_service as api_s
from models import Appointment, Module, db
from utils.enums import ApprovalStatusChoices, AttendanceChoices
from sqlalchemy import and_, or_
from flask_login import current_user
from flask_security.decorators import roles_required
import json

@roles_required('lecturer')
def index():
    #Student Dashboard
    tag = request.args.get('tag')

    upcoming_appointments = api_ctrl.fetch_lecturer_appointments().filter(and_(Appointment.approval_status == ApprovalStatusChoices.APPROVED, Appointment.attendance_status == AttendanceChoices.PENDING)).order_by(Appointment.date.asc()).all()
    old_appointments = api_ctrl.fetch_lecturer_appointments().filter(and_( or_(Appointment.approval_status == ApprovalStatusChoices.APPROVED, Appointment.approval_status == ApprovalStatusChoices.DECLINED, Appointment.approval_status == ApprovalStatusChoices.RESCHEDULED), Appointment.attendance_status != AttendanceChoices.PENDING)).order_by(Appointment.date.desc()).all()
    pending_appointments = api_ctrl.fetch_lecturer_appointments().filter(Appointment.approval_status == ApprovalStatusChoices.PENDING).order_by(Appointment.date.desc()).all()
    if tag==None:
        return render_template("views/lecturer/partial/Upcoming.html", upcoming_appointments=api_s.format_appointments_tile_data(upcoming_appointments))
    elif tag.lower() == "upcoming":
        return render_template("views/lecturer/partial/Upcoming.html", upcoming_appointments=api_s.format_appointments_tile_data(upcoming_appointments))
    elif tag.lower() == "history":
        return render_template("views/lecturer/partial/History.html", old_appointments=api_s.format_appointments_tile_data(old_appointments))
    elif tag.lower() == "pending":
        return render_template("views/lecturer/partial/Pending.html", pending_appointments=api_s.format_appointments_tile_data(pending_appointments))
    else:
        return redirect('/lecturer?tag=Upcoming')

@roles_required('lecturer')
def my_timeslots():
    return render_template("views/lecturer/TimeAvailable.html", current_user=current_user)

@roles_required('lecturer')
def manage():
    lecturer_staff_number = request.args.get('lecturer')
    print(lecturer_staff_number)

    if lecturer_staff_number == None:
        module_data = json.loads(api_ctrl.get_all_modules().data)
        return render_template('views/lecturer/Manage.html', modules=module_data, allow_edit=False)
    elif lecturer_staff_number == current_user.lecturer.staff_number:
        module_data = json.loads(api_ctrl.get_modules_by_lecture_staff_number(lecturer_staff_number).data)
        return render_template('views/lecturer/ManageLecturer.html', modules=module_data, allow_edit=True)
    else:
        return redirect('/lecturer/manage')

@roles_required('lecturer')
def add_module():
    return render_template('views/lecturer/AddToMyModules.html')

@roles_required('lecturer')
def remove_module():
    module_code = request.args.get('module')

    if module_code:
        module_query = db.session.query(Module).filter(Module.code == module_code).first()
        if module_query:
            if module_query.lecturer_id == current_user.lecturer.id:
                module_query.lecturer_id = None
                db.session.add(module_query)
                db.session.commit()

    return redirect('/lecturer/manage?lecturer=%s' % (current_user.lecturer.staff_number))

@roles_required('lecturer')
def redirect_to_manage():
    return redirect('/lecturer/manage?lecturer=%s' % (current_user.lecturer.staff_number))

