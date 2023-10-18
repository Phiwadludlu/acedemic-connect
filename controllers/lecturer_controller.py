from flask import request, render_template
from services.test_db import appointments
from datetime import datetime

def index():
    #Student Dashboard
    tag = request.args.get('tag')
    
    if tag==None:
        return render_template("views/lecturer/partial/Upcoming.html", upcoming_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "upcoming":
        return render_template("views/lecturer/partial/Upcoming.html", upcoming_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "history":
        return render_template("views/lecturer/partial/History.html", old_appointments=appointments(), datetime=datetime)
    elif tag.lower() == "pending":
        return render_template("views/lecturer/partial/Pending.html", pending_appointments=appointments(), datetime=datetime)


