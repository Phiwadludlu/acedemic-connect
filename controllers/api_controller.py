import json 
from flask import request, jsonify
from models import db, Appointment, Module, TimeSlot
from datetime import datetime
from utils.enums import ApprovalStatusChoices,AttendanceChoices
from flask_login import current_user
from services.api_service import format_timeslot_data, format_module_data
from flask_security import auth_required
import uuid

@auth_required()
def schedule_appointment():
    req_data = request.data
    form_data = json.loads(req_data)
    
    appointment_module_code = form_data["appointment_module_code"]
    appointment_timeslot_id = form_data["appointment_timeslot_id"]
    appointment_reason = form_data["appointment_reason"]
    appointment_date = form_data["appointment_date"]
    appointment_uuid = str(uuid.uuid1())

    try:
        selected_module = db.session.query(Module).filter(Module.code == appointment_module_code).first()
        selected_timeslot = db.session.query(TimeSlot).filter(TimeSlot.id == appointment_timeslot_id).first()
        new_appointment = Appointment(date=datetime.fromisoformat(appointment_date),appointment_reason=appointment_reason, approval_status=ApprovalStatusChoices.PENDING,   lecturer_id=selected_module.lecturer.id, student_id=current_user.student.id, module_id=selected_module.id, timeslot_id=selected_timeslot.id, attendance_status=AttendanceChoices.PENDING, appointment_uuid=appointment_uuid)

        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({"code" : 1}), 200
    except:
        return jsonify({"code" : -1}), 500

def fetch_modules():
    all_modules = db.session.query(Module).all()
    return format_module_data(all_modules), 200

@auth_required()
def fetch_timeslots_by_module():
    data = request.data
    unloaded = json.loads(data)

    module_code = unloaded['module_code']

    module_query = Module.query.filter(Module.code == module_code).first()
    timeslots = TimeSlot.query.filter(module_query.lecturer_id == TimeSlot.lecturer_id).all()

    return format_timeslot_data(timeslots)