from flask import request, redirect, render_template
from services.test_db import appointments
from datetime import datetime
from flask_login import current_user
from flask_security.decorators import roles_required


@roles_required('student')
def index():
    #Student Dashboard
    tag = request.args.get('tag')
    
    if tag==None:
        return render_template("views/student/partial/Upcoming.html", upcoming_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "upcoming":
        return render_template("views/student/partial/Upcoming.html", upcoming_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "history":
        return render_template("views/student/partial/History.html", old_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "pending":
        return render_template("views/student/partial/Pending.html", pending_appointments=appointments(), datetime=datetime)
    else:
        return redirect('/student?tag=Upcoming')
    
@roles_required('student')
def book_appointment():
    #Booking an appointment
    return render_template("views/student/BookAppointment.html", current_user=current_user)

