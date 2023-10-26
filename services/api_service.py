from flask import jsonify
from datetime import datetime
from models import db, Student

def format_timeslot_data(timeslots):
    skeleton = [
        {'day' : 'Monday', 'timeslots' : []},
        {'day' : 'Tuesday', 'timeslots' : []},
        {'day' : 'Wednesday', 'timeslots' : []},
        {'day' : 'Thursday', 'timeslots' : []},
        {'day' : 'Friday', 'timeslots' : []}
    ]

    for slot in timeslots:
        if slot.day == 'Monday':
            skeleton[0]['timeslots'].\
                append({
                    "timeslot_id" : slot.id,
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                })
        if slot.day == 'Tuesday':
            skeleton[1]['timeslots'].\
                append({
                    "timeslot_id" : slot.id,
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                })
        if slot.day == 'Wednesday':
            skeleton[2]['timeslots'].\
                append({
                    "timeslot_id" : slot.id,
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                })
        if slot.day == 'Thursday':
            skeleton[3]['timeslots'].\
                append({
                    "timeslot_id" : slot.id,
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                })
        if slot.day == 'Friday':
            skeleton[4]['timeslots'].\
                append({
                    "timeslot_id" : slot.id,
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                })

    return jsonify(skeleton)

def format_timeslot_label_data(timeslots):
    tmp = []

    for slot in timeslots:
        schema = {
            "day" : slot.day,
            "timeslots" : {
                "timeslot_id" : slot.id, 
                "period" : {
                    "start_time" : slot.start_time.isoformat(timespec="minutes"), 
                    "end_time" : slot.end_time.isoformat(timespec="minutes")
                }
            }
        }
        tmp.append(schema)

    result = merge_timeslots(tmp)
    return jsonify(result)

def merge_timeslots(data):
    merged_data = {}  # Dictionary to store merged data
    for item in data:
        day = item['day']
        if day not in merged_data:
            # If 'day' is not in merged_data, initialize it with the current item's 'timeslots'
            merged_data[day] = {'day': day, 'timeslots': [item['timeslots']]}
        else:
            # If 'day' is already in merged_data, append the 'timeslots' to the existing list
            merged_data[day]['timeslots'].append(item['timeslots'])

    # Convert the values of the merged_data dictionary to a list
    result = list(merged_data.values())
    return result

def format_module_data(data):

    result = []
    for item in data:
        schema = {
            "id" : item.id,
            "code" : item.code,
            "name" : item.name,
            "type" : "module",
        }
        result.append(schema)

    return jsonify(result)

def format_single_appointment_data(data):
    appointment, module, student, timeslot, old_timeslot = data
    schema = {
            "appointment_uuid" : appointment.appointment_uuid,
            "student_number" : student.student_number,
            "module_name" : module.name,
            "module_code" : module.code,
            "appointment_timeslot" : timeslot.start_time.isoformat(timespec='minutes') + "-" + timeslot.end_time.isoformat(timespec='minutes'),
            "appointment_reason" : appointment.appointment_reason,
            "approval_status" : appointment.approval_status.value,
            "is_reschedule" : appointment.is_reschedule,
            "date": appointment.date.strftime("%A, %B %d, %Y"),
            "attendance_status" : appointment.attendance_status.value,
            "old_timeslot" : old_timeslot.start_time.isoformat(timespec='minutes') + "-" + old_timeslot.end_time.isoformat(timespec='minutes') if old_timeslot else '',
        }
    return schema

def format_appointments_tile_data(data):
    result = []
    for item in data:
        appointment, timeslot = item
        student = Student.query.filter(appointment.student_id == Student.id).first()
        schema = {
                "appointment_uuid" : appointment.appointment_uuid,
                "student_fullname" : student.student_fullname,
                "day_of_week" : appointment.date.strftime("%A"),
                "day_of_month": appointment.date.day,
                "day_time" : appointment.date.strftime("%d %b") + ", " + timeslot.start_time.strftime("%I:%M %p"),
            }
        result.append(schema)
    return result