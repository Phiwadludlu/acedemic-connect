from flask import Blueprint
from controllers import api_controller as api_ctrl

"Nkaty!!!!"

api_route = Blueprint('api_routes',__name__)

api_route.add_url_rule('/schedule_appoinment','schedule_appoinment',api_ctrl.schedule_appointment, methods=['POST'])
api_route.add_url_rule('/fetch_modules','fetch_modules',api_ctrl.fetch_modules, methods=['GET'])
#api_route.add_url_rule('/fetch_timeslots_by_module','fetch_timeslots_by_module',api_ctrl.fetch_timeslots_by_module, methods=['POST'])
