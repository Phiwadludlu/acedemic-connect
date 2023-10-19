import json 
from flask import request, jsonify
from models import db, Appointment, Module
from datetime import datetime
from utils.enums import ApprovalStatusChoices,AttendanceChoices

def schedule_appointment():
    req_data = request.data
    form_data = json.loads(req_data)
    
    appointment_module = form_data["appointment_module"]
    appointment_reason = form_data["appointment_reason"]
    appointment_date = form_data["appointment_date"]
    appointment_timeslot = 1

    selected_module = db.session.query(Module).filter(Module.code == appointment_module).first()
    new_appointment = Appointment(date=datetime.fromisoformat(appointment_date),appointment_reason=appointment_reason)

    return jsonify({"message":"hi"}), 200
