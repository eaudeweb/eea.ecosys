import flask


library = flask.Blueprint('library', __name__)


@library.route('/')
def home():
    return flask.Response()