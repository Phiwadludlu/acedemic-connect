from flask import Flask
from routes.core_route import core_route

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    return app


#Flask App instane
app = create_app()


#Route Registrations here

app.register_blueprint(core_route, url_prefix = '/')


if __name__ == '__main__':
    app.run(debug=True)