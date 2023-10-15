
"""The controllers module is for business logic"""
from flask import request, render_template, flash, redirect, url_for, session
from flask_security import hash_password, anonymous_user_required, auth_required

from forms.auth_forms.sign_up_form import StudentRegisterForm, LecturerRegisterForm
from models import Student, User, Role, db, Lecturer
from utils.create_db_tables import  create_tables
@anonymous_user_required
def index():
    return render_template("views/LandingpageView.html")

def create_db_tables():

        create_tables()
        return "Done"


@anonymous_user_required
def signUp():
    return redirect(url_for('core_routes.student_sign_up'))


@anonymous_user_required
def lecturer_sign_up():
    register_lecturer_form = LecturerRegisterForm()

    if request.method == "POST":
        if register_lecturer_form.validate_on_submit():
            lecturer_role = Role.query.filter_by(id=3).first_or_404()

            # Add user to DB logic here
            new_user = User(email=register_lecturer_form.email.data,
                            password=hash_password(register_lecturer_form.password.data), active=True)
            new_user.fs_uniquifier = new_user.get_auth_token()
            new_user.is_active = True
            new_user.roles.append(lecturer_role)

            new_lecturer = Lecturer(staff_number=register_lecturer_form.staff_number.data, user=new_user)

            db.session.add(new_user)
            db.session.add(new_lecturer)
            db.session.commit()

            flash("Account created successfully", category="info")

            return redirect(url_for("security.login"))

    return render_template("components/forms/auth_forms/lecturer_form.html",
                           register_lecturer_form=register_lecturer_form)


@anonymous_user_required
def student_sign_up():
    register_student_form = StudentRegisterForm()

    if request.method == "POST":
        if register_student_form.validate_on_submit():
            student_role = Role.query.filter_by(id=2).first_or_404()

            # Add user to DB logic here
            new_user = User(email=register_student_form.email.data,
                            password=hash_password(register_student_form.password.data), active=True)
            new_user.fs_uniquifier = new_user.get_auth_token()
            new_user.is_active = True
            new_user.roles.append(student_role)

            new_student = Student(student_number=register_student_form.student_number.data, user=new_user)

            db.session.add(new_user)
            db.session.add(new_student)
            db.session.commit()

            flash("Account created successfully", category="info")

            return redirect(url_for("security.login"))

    return render_template("components/forms/auth_forms/student_form.html", register_student_form=register_student_form)


@auth_required()
def proxy_redirect():
    user_id = session["_user_id"]
    current_user = User.query.filter_by(fs_uniquifier=user_id).first()

    if current_user.has_role('student'):

        return redirect(url_for("student_route.index"))

    elif current_user.has_role('lecturer'):

        return redirect(url_for("lecturers.lecturerMain"))