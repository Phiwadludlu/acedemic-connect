from flask import Blueprint
import controllers.student_controller as sc
"""This file houses all core routes which are basic routes for the website 

    -khanya

"""

student_route = Blueprint('student_route',__name__)


student_route.add_url_rule('/','index',sc.index, methods=['GET'])

student_route.add_url_rule('/appointment/new', 'book', sc.book_appointment,methods=['GET', 'POST'])
