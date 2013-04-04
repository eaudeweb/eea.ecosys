import flask
from flask.ext.assets import Environment, Bundle
from werkzeug import SharedDataMiddleware

import jinja2

from ecosys.models import db
from ecosys.auth import login_manager
# import blueprints
from ecosys import library, resource, auth, frameservice

from .assets import BUNDLE_JS, BUNDLE_CSS


DEFAULT_CONFIG = {
    'MONGODB_SETTINGS': {
        'DB': 'ecosys',
    },
    'ASSETS_DEBUG': True,
    'CSRF_ENABLED': False,
    'LDAP_ENCODING': 'utf-8',
    'LDAP_USER_DN': "uid=%s,ou=Users,o=EIONET,l=Europe",
    'LDAP_USER_SCHEMA': {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
        'phone_number': 'telephoneNumber',
        'organisation': 'o',
        'uid': 'uid',
    }
}

BLUEPRINTS = (
    library,
    resource,
    auth,
)


def create_app(instance_path=None, config={}):
    app = flask.Flask(__name__, instance_path=instance_path,
                      instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, BLUEPRINTS)
    configure_assets(app)
    configure_static(app)
    configure_authentication(app)
    configure_templating(app)
    db.init_app(app)
    return app


def configure_app(app, config):
    app.config.update(DEFAULT_CONFIG)
    app.config.from_pyfile('settings.py', silent=True)
    app.config.update(config)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        blueprint.initialize_app(app)


def configure_assets(app):
    assets = Environment(app)
    js = Bundle(*BUNDLE_JS, filters='jsmin', output='output/packed.js')
    css = Bundle(*BUNDLE_CSS, filters='cssmin', output='output/packed.css')

    assets.register('packed_js', js)
    assets.register('packed_css', css)

def configure_static(app):
    if app.config['DEBUG']:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            "/static/files": app.config['UPLOADED_FILES_DEST'],
        })

def configure_authentication(app):
    login_manager.setup_app(app)

def configure_templating(app):
    original_loader = app.jinja_env.loader
    func_loader = jinja2.FunctionLoader(frameservice.load_template)
    app.jinja_env.loader = jinja2.ChoiceLoader([func_loader, original_loader])
