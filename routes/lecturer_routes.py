from flask import Blueprint
import controllers.lecturer_controller as lc


lecturer_route = Blueprint("lecturer_route",__name__)

lecturer_route.add_url_rule("","index", lc.index, methods=["GET"])
lecturer_route.add_url_rule("/timeslots","lecturer_timeslots", lc.my_timeslots, methods=["GET"])

lecturer_route.add_url_rule("/manage","lecturer_manage", lc.manage, methods=["GET"])
lecturer_route.add_url_rule("/manage/","", lc.redirect_to_manage, methods=["GET"])
lecturer_route.add_url_rule("/manage/add","lecturer_add_module", lc.add_module, methods=["GET"])
lecturer_route.add_url_rule("/manage/remove","lecturer_remove_module", lc.remove_module, methods=["GET"])
