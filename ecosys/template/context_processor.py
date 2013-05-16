from flask.ext import login as flask_login


def inject_user():
    return {
        'user': flask_login.current_user
    }
