import flask
import logging
import jinja2

from webassets.filter import get_filter

from flask.ext.assets import Environment, Bundle
from werkzeug import SharedDataMiddleware
from raven.contrib.flask import Sentry
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler
from path import path

from ecosys.models import db
from ecosys.auth import login_manager
from ecosys import library, resource, auth, frameservice
from ecosys.admin import admin
from ecosys.template import inject_user, inject_countries
from ecosys.template import (filter_eu, filter_eea, filter_eionet,
                             filter_eun22, to_json)

from .assets import (BUNDLE_JS, BUNDLE_CSS, BUNDLE_IE_CSS7, BUNDLE_IE_CSS8,
                     BUNDLE_IE_CSS9)


DEFAULT_CONFIG = {
    'MONGODB_SETTINGS': {
        'DB': 'ecosys',
    },
    'ROOT_PATH': path(__file__).dirname().expand(),
    'ASSETS_DEBUG': False,
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
    },
    'API_URL': 'http://194.30.43.115:3000/api/v1/ecosystem_assessments',
    'SPARQL_ENDPOINT': 'http://semantic.eea.europa.eu/sparql',
}


BLUEPRINTS = (
    library,
    resource,
    auth,
)


sentry = Sentry()


def create_app(instance_path=None, config={}):
    app = flask.Flask(__name__, instance_path=instance_path,
                      instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, BLUEPRINTS)
    configure_assets(app)
    configure_static(app)
    configure_authentication(app)
    configure_templating(app)
    configure_error_pages(app)
    configure_sentry(app)
    db.init_app(app)
    admin.init_app(app)
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
    css_rewrite = get_filter('cssrewrite', replace={'/static/':'../'})
    css = Bundle(*BUNDLE_CSS, filters=(css_rewrite, 'cssmin'),
                 output='output/packed.css')
    ie_css7 = Bundle(*BUNDLE_IE_CSS7, filters='cssmin', output='output/ie7.css')
    ie_css8 = Bundle(*BUNDLE_IE_CSS8, filters='cssmin', output='output/ie8.css')
    ie_css9 = Bundle(*BUNDLE_IE_CSS9, filters='cssmin', output='output/ie9.css')

    assets.register('packed_js', js)
    assets.register('packed_css', css)
    assets.register('packed_ie_css7', ie_css7)
    assets.register('packed_ie_css8', ie_css8)
    assets.register('packed_ie_css9', ie_css9)

def configure_static(app):
    if app.config['DEBUG']:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            "/static/files": app.config['UPLOADED_FILES_DEST'],
        })

def configure_authentication(app):
    login_manager.setup_app(app)


def configure_error_pages(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template('404.html'), 404

    @app.errorhandler(500)
    def page_error(e):
        return flask.render_template('500.html'), 500

    @app.route('/crashme')
    def crashme():
        raise Exception


def configure_templating(app):
    original_loader = app.jinja_env.loader
    func_loader = jinja2.FunctionLoader(frameservice.load_template)
    app.jinja_env.loader = jinja2.ChoiceLoader([func_loader, original_loader])
    app.context_processor(inject_user)
    app.context_processor(inject_countries)
    app.add_template_filter(filter_eu)
    app.add_template_filter(filter_eea)
    app.add_template_filter(filter_eionet)
    app.add_template_filter(filter_eun22)
    app.add_template_filter(to_json)


def configure_sentry(app):
    sentry.init_app(app)
    sentry_handler = SentryHandler(sentry.client)
    sentry_handler.setLevel(logging.WARN)
    setup_logging(sentry_handler)
