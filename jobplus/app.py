# coding = utf-8
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.config import configs
from jobplus.models import db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    Migrate(app, db)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from .handles import front

    app.register_blueprint(front)