import flask_migrate
import flask_security
from flask import Flask
from flask_mailman import EmailMultiAlternatives, Mail
from flask_cors import CORS

from forms.auth_forms.sign_up_form import StudentRegisterForm
from routes.core_route import core_route
from models import db,User,Role
from routes.lecturer_routes import lecturer_route
from routes.student_routes import student_route
from routes.api_route import api_route
from utils.celery.celery import celery_init_app

from utils.celery.flask_mail import MyMailUtil, mail 

from controllers import core_controller as cl


def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config.from_object('config')

    return app


#Flask App instane
app = create_app()
db.init_app(app)

mail.init_app(app)
flask_migrate.Migrate(app=app, db=db)

@app.errorhandler(404)
def handle_not_found(e):
    return cl.not_found(e)


#Authentication config
user_datastore = flask_security.SQLAlchemySessionUserDatastore(session=db.session, user_model=User, role_model=Role)

security = flask_security.Security(app=app, datastore=user_datastore, register_form=StudentRegisterForm)

security.init_app(app=app,register_blueprint=False, mail_util=MyMailUtil)


#Route Registrations here

app.register_blueprint(core_route, url_prefix = '/')
app.register_blueprint(student_route,url_prefix = '/student')
app.register_blueprint(lecturer_route, url_prefix = '/lecturer')
app.register_blueprint(api_route, url_prefix = '/v1/api')



if __name__ == '__main__':
    app.run(debug=True)