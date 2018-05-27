from flask import Flask, render_template
from src.mod_auth.usersAuthRestApi import auth
from src.contactBook.contactsRestApi import contactBook
from src import app
from mod_auth.models import db


def create_app(config_obj):
    " Factory for creating app "
    load_config(app, config_obj)
    initialize_app(app)
    register_blueprints(app)
    register_errorhandlers(app)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
    return app


def load_config(app, config_obj):
    app.config.from_object(__name__)
    app.config.from_object(config_obj)


def initialize_app(app):
    " Do any one-time initialization of the src prior to serving "
    app.static_folder = app.config['STATIC_DIR']

    @app.teardown_appcontext
    def remove_session(response):
        db.session.remove()
        return response


def register_blueprints(app):
    " Registers blueprint routes on src "
    app.register_blueprint(contactBook)
    app.register_blueprint(auth)


def register_errorhandlers(app):
    " Register custom error pages "

    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{}.html'.format(error_code)), error_code

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)

