from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .auth_models import User,Role,RoleUsers
from .student_model import Student
from .lecturer_model import Lecturer