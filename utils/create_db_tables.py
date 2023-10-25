from models import db,Role
from services import populate_moduletable, populate_qualificationtable


def create_tables():
    from app import app
    with app.app_context():
        db.create_all()
        create_roles()
        db.session.flush()
        populate_qualificationtable.run()
        populate_moduletable.run()



def create_roles():
    admin_role = Role(name="admin", description="admin role")
    student_role = Role(name="student", description="student role")
    lecturer_role = Role(name="lecturer", description="lecturer role")

    db.session.add(admin_role)
    db.session.add(student_role)
    db.session.add(lecturer_role)

    db.session.commit()

