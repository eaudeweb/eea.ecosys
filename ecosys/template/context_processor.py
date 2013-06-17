from flask.ext import login as flask_login
from ecosys.models import Country


def inject_user():
    return {
        'user': flask_login.current_user
    }


def inject_countries():
    return {
        'countries': Country.objects.all(),
    }
