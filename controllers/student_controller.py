from flask import render_template
def index():
    #Student Dashboard
    return render_template("views/student_views/studentDashboard.html")

def book_appointment():
    #Booking an appointment

    return render_template("views/student_views/studentBookAppointment.html")