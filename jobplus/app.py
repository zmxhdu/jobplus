# coding = utf-8
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.config import configs


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    return app