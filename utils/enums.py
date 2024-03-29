import enum

class ApprovalStatusChoices(enum.Enum):

    APPROVED = 'Approved'
    DECLINED = 'Declined'
    RESCHEDULED = 'Rescheduled'
    PENDING = 'Pending'


class AttendanceChoices (enum.Enum):

    PRESENT = 'Present'
    MISSED = 'Missed'
    PENDING = 'Pending'
    RESCHEDULED = 'Rescheduled'
    DECLINED = 'Declined'

class DayChoices(enum.Enum):

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"

class NotificationStatus(enum.Enum):

    Pending = 0
    Read = 1