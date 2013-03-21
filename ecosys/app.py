import flask
from models import db

# import blueprints
from .library import library


DEFAULT_CONFIG = {
    'MONGODB_SETTINGS': {
        'DB': 'ecosys',
    }
}

BLUEPRINTS = (
    library,
)


def create_app(instance_path=None, config={}):
    app = flask.Flask(__name__, instance_path=instance_path,
                      instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, BLUEPRINTS)
    db.init_app(app)
    return app


def configure_app(app, config):
    app.config.update(DEFAULT_CONFIG)
    app.config.from_pyfile('settings.py', silent=True)
    app.config.update(config)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
