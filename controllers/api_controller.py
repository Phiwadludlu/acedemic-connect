import json 
from flask import request, jsonify, redirect
from models import db, Appointment, Module, TimeSlot, RescheduledApproval, Student, Lecturer
from datetime import datetime
from utils.enums import ApprovalStatusChoices,AttendanceChoices
from flask_login import current_user
from services.api_service import format_timeslot_data, format_module_data, format_appointments_tile_data, format_timeslot_label_data
from flask_security import auth_required
from flask_security.decorators import roles_required

import uuid
from sqlalchemy import and_

@roles_required('student')
def schedule_appointment():
    req_data = request.data
    form_data = json.loads(req_data)
    
    appointment_module = form_data["appointment_module_code"]
    appointment_reason = form_data["appointment_reason"]
    appointment_date = form_data["appointment_date"]
    appointment_timeslot = form_data["appointment_timeslot_id"]
    appointment_uuid = str(uuid.uuid1())

    print(form_data)

    try:
        selected_module = db.session.query(Module).filter(Module.code == appointment_module).first()
        selected_timeslot = db.session.query(TimeSlot).filter(TimeSlot.id == appointment_timeslot).first()
        new_appointment = Appointment(date=datetime.fromisoformat(appointment_date),appointment_reason=appointment_reason, approval_status=ApprovalStatusChoices.PENDING,   lecturer_id=selected_module.lecturer.id, student_id=current_user.student.id, module_id=selected_module.id, timeslot_id=selected_timeslot.id,   attendance_status=AttendanceChoices.PENDING, appointment_uuid=appointment_uuid)

        selected_timeslot.is_available = False

        db.session.add(selected_timeslot)
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"code" : 1}), 200
    except:
        return jsonify({"code" : -1}), 500

@roles_required('student')
def fetch_student_appointments():
    all_appoinments = db.session.query(Appointment, TimeSlot).filter(and_(Appointment.student_id == current_user.student.id, Appointment.timeslot_id == TimeSlot.id, Student.id == current_user.student.id))
    return all_appoinments

@roles_required('lecturer')
def fetch_lecturer_appointments():
    all_appoinments = db.session.query(Appointment,TimeSlot).filter(and_(Appointment.lecturer_id == current_user.lecturer.id, Appointment.timeslot_id == TimeSlot.id))
    return all_appoinments

@auth_required()
def get_appointment_by_approval_status():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if 'approval_status' in form_data:
        status = form_data['approval_status']
        filtered_appointments = Appointment.query.filter_by(approval_status=status).all()
        return jsonify(filtered_appointments), 200

@roles_required('lecturer')
def get_appointments_by_lecture_staff_number():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if "lecture_staff_number" in form_data:
        lecturer_staff_number = form_data["lecturer_staff_number"]
        lecturer = Lecturer.query.filter(Lecturer.staff_number == lecturer_staff_number).first()
        appointments = Appointment.query.filter(Appointment.lecturer_id == lecturer.id)
        return jsonify(appointments), 200

@roles_required('student')
def get_appointments_by_student_number():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if "student_number" in form_data:
        student_number = form_data["student_number"]
        student = Student.query.filter(Student.student_number == student_number).first()
        appointments = Appointment.query.filter(Appointment.student_id == student.id)
        return jsonify(appointments), 200

@auth_required()
def get_appointments_by_module_code():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if 'module_code' in form_data:
        module_code = form_data['module_code']
        module_record = Module.query.filter(Module.code == module_code).first()
        appointments = Appointment.query.filter(module_record.id == Appointment.module_id).all()
        return jsonify(appointments), 200

@auth_required()
def get_appointments_by_attendance_status():
    req_data = request.data
    form_data = json.loads(req_data)

    if 'attendance_status' in form_data:
        status = form_data['attendance_status']
        appointments = Appointment.query.filter_by(attendance_status =status).all()
        return jsonify(appointments), 200
    
@auth_required()
def get_all_modules():
    all_modules = db.session.query(Module).all()
    return format_module_data(all_modules)

@roles_required('lecturer')
def add_to_my_modules():
    try:
        data = request.data
        unloaded = json.loads(data)

        all_modules = unloaded['all_modules']
        print(all_modules)

        for module_code in all_modules:
            module_query = db.session.query(Module).filter(Module.code == module_code).first()

            if module_query.lecturer_id == None:
                module_query.lecturer_id = current_user.lecturer.id
                db.session.add(module_query)
            
        db.session.commit()

        return jsonify({'code' : 1}) # all is well
    except:
        return jsonify({'code' : -2}) # server error 

@auth_required()
def get_single_module_by_module_code(module_code):
    module = Module.query.filter(Module.code==module_code).first()
    return jsonify(module)

@auth_required()
def get_modules_by_lecture_staff_number(staff_number):
    lecturer = Lecturer.query.filter(Lecturer.staff_number == staff_number).first()
    all_modules = Module.query.filter(Module.lecturer_id == lecturer.id)
    return format_module_data(all_modules)

@auth_required() 
def get_reschedule_approval_by_student_number():
    req_data = request.data
    form_data = json.load(req_data)

    if "student_number" in form_data:
        student_number = form_data["student_number"]
        student = Student.query.filter(Student.student_number == student_number).first()
        student_appointments_needing_approval = Appointment.query.filter(and_(Appointment.student_id == student.id, Appointment.approval_status==ApprovalStatusChoices.PENDING))
        return jsonify(student_appointments_needing_approval), 200

@auth_required()
def get_reschedule_approval_by_staff_number():
    req_data = request.data
    form_data = json.load(req_data)
    
    if "staff_number" in form_data:
        staff_number = form_data["staff_number"]
        lecturer = Lecturer.query.filter(Lecturer.staff_number == staff_number).first()
        lecturer_appointments_needing_approval = Appointment.query.filter(and_(Appointment.lecturer_id == lecturer.id, Appointment.approval_status==ApprovalStatusChoices.PENDING))
        return jsonify(lecturer_appointments_needing_approval), 200

@auth_required()
def get_timeslot_by_day():
    req_data = request.data
    form_data = json.loads(req_data)

    if 'day' in form_data:
        day = form_data['day']
        timeslots = TimeSlot.query.filter(TimeSlot.day == day).all()

@auth_required()
def get_timeslots_by_staff_number():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if 'staff_number' in form_data:
        staff_number = form_data['staff_number']
        lecturer = Lecturer.query.filter(Lecturer.staff_number == staff_number).first()
        timeslots = TimeSlot.query.filter(and_(TimeSlot.lecturer_id == lecturer.id, TimeSlot.is_available == True)).all()
        return format_timeslot_data(timeslots), 200

@auth_required()
def get_all_timeslots():
    timeslots = TimeSlot.query.all()
    return format_timeslot_data(timeslots), 200

@auth_required()
def get_timeslots_by_module():

    req_data = request.data
    form_data = json.loads(req_data)
    
    if 'module_code' in form_data:
        module_code = form_data['module_code']
        module = Module.query.filter(Module.code == module_code).first()
        timeslots = TimeSlot.query.filter(and_(TimeSlot.lecturer_id == module.lecturer_id, TimeSlot.is_available == True)).all()
        return format_timeslot_label_data(timeslots)

@auth_required()
def update_timeslots_by_staff_number():
    req_data = request.data
    form_data = json.loads(req_data)
    
    if 'staff_number' in form_data:
        staff_number = form_data['staff_number']
        staged_for_removal = form_data['staged_for_removal']
        days = form_data['days']
        new_timeslots = [{**day, 'timeslots': [slot for slot in day['timeslots'] if (slot['timeslot_id'] == '' and slot['start_time'] != '' and slot['end_time'] != '')]} for day in days]
        if staff_number == current_user.lecturer.staff_number:
            lecturer = Lecturer.query.filter(Lecturer.staff_number == staff_number).first()
            timeslots = TimeSlot.query.filter(TimeSlot.lecturer_id == lecturer.id).all()
            for record in timeslots:
                if record.id in staged_for_removal:
                    db.session.delete(record)

            for item in new_timeslots:
                for slot in item['timeslots']:
                    new_slot = TimeSlot(day=item['day'],start_time=datetime.strptime(slot['start_time'], '%H:%M').time(),end_time=datetime.strptime(slot['end_time'], '%H:%M').time(), lecturer_id=lecturer.id)
                    db.session.add(new_slot)
            
            db.session.commit()
            return jsonify({"code": 1})
        else:
            return jsonify({"code":-1}) # not allowed because dont own timeslot

@auth_required()
def update_appointment_student_attendance():
    req_data = request.data
    form_data = json.loads(req_data)

    if 'appointment_uuid' in form_data:
        appointment_uuid = form_data['appointment_uuid']
        student_attendance = form_data['student_attendance']
        appointment = Appointment.query.filter(Appointment.appointment_uuid == appointment_uuid).first()
        timeslot = TimeSlot.query.filter(TimeSlot.id == appointment.timeslot_id).first()

        if student_attendance == 'Present':
            appointment.attendance_status = AttendanceChoices.PRESENT
        if student_attendance == 'Missed':
            appointment.attendance_status = AttendanceChoices.MISSED

        timeslot.is_available = True

        db.session.add(timeslot)
        db.session.add(appointment)
        db.session.commit()

        return jsonify({"code": 1})
    else:
        return jsonify({"code": -1})
        
