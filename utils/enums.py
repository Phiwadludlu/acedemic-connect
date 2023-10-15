import enum

class ApprovalStatusChoices(enum.Enum):

    APPROVED = 'Approved'
    DECLINED = 'Declined'
    RESCHEDULED = 'Rescheduled'


class AttendanceChoices (enum.Enum):

    PRESENT = 'Present'
    MISSED = 'Missed'
    PENDING = 'Pending'


class DayChoices(enum.Enum):

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
