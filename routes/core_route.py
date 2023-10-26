from flask import Blueprint
import controllers.core_controller as core 

"""This file houses all core routes which are basic routes for the website 

    -khanya

"""

core_route = Blueprint('core_routes',__name__)


core_route.add_url_rule('/','index',core.index, methods=['GET'])
core_route.add_url_rule('/create-tables', view_func=core.create_db_tables, methods=['GET'])
core_route.add_url_rule('/register', view_func=core.signUp, methods=['GET','POST'])
core_route.add_url_rule('/register/lecturer', view_func=core.lecturer_sign_up, methods=['GET', 'POST'])
core_route.add_url_rule('/register/student', view_func=core.student_sign_up, methods=['GET', 'POST'])
core_route.add_url_rule('/redirect-proxy', view_func=core.proxy_redirect, methods=['GET'])

core_route.add_url_rule("/calendar", 'calendar', core.calendar, methods=['GET'])
core_route.add_url_rule("/notifications", 'notifications', core.notifications, methods=['GET'])
core_route.add_url_rule("/appointment/<appointment_uuid>","single_appointment", core.single_appointment, methods=["GET"])
core_route.add_url_rule("/appointment/<appointment_uuid>/reschedule","reschedule_appointment", core.reschedule_appointment, methods=["GET"])
core_route.add_url_rule("/appointment/approve/<appointment_uuid>","approve_appointment", core.approve_appointment, methods=["GET"])
core_route.add_url_rule("/appointment/decline/<appointment_uuid>","decline_appointment", core.decline_appointment, methods=["GET"])

core_route.add_url_rule("/confirm", "confirm_account", core.confirm_account, methods=['GET'])