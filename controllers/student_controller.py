from flask import request, render_template
from services.test_db import appointments
from datetime import datetime

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

def book_appointment():
    #Booking an appointment
    return render_template("views/student/BookAppointment.html")

