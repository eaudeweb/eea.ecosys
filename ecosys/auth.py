import base64
from functools import wraps
import datetime

from flask import (Blueprint, request, render_template, redirect, url_for,
                   flash, g)
from flask.ext.login import LoginManager
from flask.ext import wtf
from flask.ext import login as flask_login


from ecosys.forms import LoginForm
from ecosys.models import User
from ecosys import plugldap


auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def load_user_in_g():
    g.user = flask_login.current_user


def initialize_app(app):
    app.register_blueprint(auth)
    app.before_request(load_user_in_g)

def get_user(userid):
    """ Get or create user document in local db, using info in LDAP """
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        user_info = plugldap.user_info(userid)
        if user_info:
            (user, created) = User.objects.get_or_create(id=user_info['uid'],
                                                          defaults=user_info)
            return user
        else:
            return None
login_manager.user_loader(get_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = request.form['username'], request.form['password']
        if plugldap.login_user(username, password):
            user = get_user(username)
            flask_login.login_user(user)
            flash('Logged in successfully as %s %s (%s).' %
                  (user.first_name, user.last_name, user.id))
            user.last_login = datetime.datetime.utcnow()
            user.save(safe=False)
            resp = redirect(request.args.get("next") or url_for('library.home'))
            resp.set_cookie("__ac",
                            base64.b64encode("%s:%s" % (username, password)))
            return resp
        else:
            flash('Bad username or password.')
    # if request.args.get("next"):
        # flash("You need to login in order to continue.")
    return render_template('login.html', form=form)


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash("You have successfully logged out.")
    resp = redirect(url_for('library.home'))
    resp.set_cookie("__ac", "")
    return resp

def get_current_user_roles():
    user = flask_login.current_user
    if user.is_anonymous():
        return []
    else:
        return user.roles

def requires_role(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if role not in get_current_user_roles():
                return redirect(url_for('auth.unauthorized'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@auth.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")
