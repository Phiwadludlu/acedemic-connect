from flask import Blueprint
import controllers.lecturer_controller as lc


lecturer_route = Blueprint("lecturer_route",__name__)

lecturer_route.add_url_rule("","index", lc.index, methods=["GET"])


