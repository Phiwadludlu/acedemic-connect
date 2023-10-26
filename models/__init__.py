from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

from .auth_models import User,Role,RoleUsers
from .student_model import Student
from .lecturer_model import Lecturer
from .appointment_model import Appointment
from .module_model import Module
from .qualification_model import Qualification
from .qualification_period import QualificationPeriod
from .rescheduled_approval_model import RescheduledApproval
from .timeslot_model import TimeSlot
from .notification_model import Notification