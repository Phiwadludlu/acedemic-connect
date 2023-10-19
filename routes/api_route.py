from flask import Blueprint
from controllers.api_controller import schedule_appointment

"Nkaty!!!!"

api_route = Blueprint('api_routes',__name__)

api_route.add_url_rule('/schedule_appoinment','schedule_appoinment',schedule_appointment, methods=['POST'])
