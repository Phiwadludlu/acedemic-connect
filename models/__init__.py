from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .auth_models import User,Role,RoleUsers
from .student_model import Student
from .lecturer_model import Lecturer
from .appointment_model import Appointment
from .module_model import Module
from .qualification_model import Qualification
from .qualification_period import QualificationPeriod
from .rescheduled_approval_model import RescheduledApproval
from .timeslot_model import TimeSlot