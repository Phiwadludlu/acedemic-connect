from flask import Blueprint
from controllers import api_controller as api_ctrl

"Nkaty!!!!"

api_route = Blueprint('api_routes',__name__)

api_route.add_url_rule('/schedule_appointment', 'schedule_appointment',api_ctrl.schedule_appointment, methods=['POST'])
api_route.add_url_rule('/get_all_modules', 'fetch_modules',api_ctrl.get_all_modules, methods=['GET'])
api_route.add_url_rule('/get_timeslots_by_module', 'fetch_timeslots_by_module',api_ctrl.get_timeslots_by_module, methods=['POST'])
api_route.add_url_rule('/get_appointment_by_approval_status', 'get_appoinment_by_approval_status',api_ctrl.get_appointment_by_approval_status, methods=['POST'])
api_route.add_url_rule('/get_appointments_by_lecture_staff_number', 'get_appointments_by_lecture_staff_number',api_ctrl.get_appointments_by_lecture_staff_number, methods=['POST'])
api_route.add_url_rule('/get_appointments_by_student_number', 'get_appointments_by_student_number',api_ctrl.get_appointments_by_student_number, methods=['POST'])
api_route.add_url_rule('/get_appointments_by_module_code', 'get_appoinments_by_module_code',api_ctrl.get_appointments_by_module_code, methods=['POST'])
api_route.add_url_rule('/get_appointments_by_attendance_status', 'get_appointments_by_attendance_status',api_ctrl.get_appointments_by_attendance_status, methods=['POST'])
api_route.add_url_rule('/get_single_module_by_module_code', 'get_single_module_by_module_code',api_ctrl.get_single_module_by_module_code, methods=['POST'])
api_route.add_url_rule('/get_modules_by_lecture_staff_number', 'get_modules_by_lecture_staff_number',api_ctrl.get_modules_by_lecture_staff_number, methods=['POST'])
api_route.add_url_rule('/get_reschedule_approval_by_student_number', 'get_reschedule_approval_by_student_number',api_ctrl.get_reschedule_approval_by_student_number, methods=['POST'])
api_route.add_url_rule('/get_reschedule_approval_by_staff_number', 'get_reschedule_approval_by_staff_number',api_ctrl.get_reschedule_approval_by_staff_number, methods=['POST'])
api_route.add_url_rule('/get_timeslot_by_day', 'get_timeslot_by_day',api_ctrl.get_timeslot_by_day, methods=['POST'])
api_route.add_url_rule('/get_timeslot_by_staff_number', 'get_timeslot_by_staff_number', api_ctrl.get_timeslot_by_staff_number, methods=['POST'])
api_route.add_url_rule('/get_all_timeslots', 'get_all_timeslots',api_ctrl.get_all_timeslots, methods=['POST'])