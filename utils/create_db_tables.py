from models import db,Role



def create_tables():
    from app import app
    with app.app_context():
        db.create_all()
        create_roles()



def create_roles():
    admin_role = Role(name="admin", description="admin role")
    student_role = Role(name="student", description="student role")
    lecturer_role = Role(name="lecturer", description="lecturer role")

    db.session.add(admin_role)
    db.session.add(student_role)
    db.session.add(lecturer_role)

    db.session.commit()

