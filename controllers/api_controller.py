import json 
from flask import request, jsonify
from models import db, Appointment, Module, TimeSlot
from datetime import datetime
from utils.enums import ApprovalStatusChoices,AttendanceChoices
from flask_login import current_user
from services.api_service import format_timeslot_data, format_module_data
from flask_security import auth_required

@auth_required()
def schedule_appointment():
    req_data = request.data
    form_data = json.loads(req_data)
    
    appointment_module = form_data["appointment_module"]
    appointment_reason = form_data["appointment_reason"]
    appointment_date = form_data["appointment_date"]
    appointment_timeslot = form_data["appointment_timeslot"]

    try:
        selected_module = db.session.query(Module).filter(Module.code == appointment_module).first()
        selected_timeslot = db.session.query(TimeSlot).filter(TimeSlot.id == appointment_timeslot).first()
        new_appointment = Appointment(date=datetime.fromisoformat(appointment_date),appointment_reason=appointment_reason, approval_status=ApprovalStatusChoices.PENDING,   lecturer_id=selected_module.lecturer.id, student_id=current_user.student.id, module_id=selected_module.id, timeslot_id=selected_timeslot.id,    attendance_status=AttendanceChoices.PENDING)
    
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"code" : 1}), 200
    except:
        return jsonify({"code" : -1}), 500

def fetch_modules():
    all_modules = db.session.query(Module).all()
    return format_module_data(all_modules), 200
