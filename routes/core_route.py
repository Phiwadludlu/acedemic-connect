from flask import Blueprint
from controllers.core_controller import index, create_db_tables, signUp, lecturer_sign_up, student_sign_up, \
    proxy_redirect

"""This file houses all core routes which are basic routes for the website 

    -khanya

"""

core_route = Blueprint('core_routes',__name__)


core_route.add_url_rule('/','index',index, methods=['GET'])
core_route.add_url_rule('/create-table', view_func=create_db_tables, methods=['GET'])
core_route.add_url_rule('/register', view_func=signUp, methods=['GET','POST'])
core_route.add_url_rule('/register/lecturer', view_func=lecturer_sign_up, methods=['GET', 'POST'])
core_route.add_url_rule('/register/student', view_func=student_sign_up, methods=['GET', 'POST'])
core_route.add_url_rule('/redirect-proxy', view_func=proxy_redirect, methods=['GET'])