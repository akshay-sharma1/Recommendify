from flask import Flask
from flask_session import Session

sess = Session()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.ProdConfig')

    sess.init_app(app)

    with app.app_context():
        from application.routes import preferences, authentication, rec

        app.register_blueprint(preferences.preferences)
        app.register_blueprint(authentication.home)
        app.register_blueprint(rec.rec)

        return app
