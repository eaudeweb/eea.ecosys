import base64
from functools import wraps
import datetime

from flask import (Blueprint, request, render_template, redirect, url_for,
                   flash, g, views)
from flask.ext.login import LoginManager
from flask.ext import wtf
from flask.ext import login as flask_login


from ecosys.forms import LoginForm, ProfileForm
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
    """ Get or create user document in local db, using info in LDAP. """
    try:
        return (User.objects.get(id=userid), False)
    except User.DoesNotExist:
        user_info = plugldap.user_info(userid)
        if user_info:
            (user, created) = User.objects.get_or_create(id=user_info['uid'],
                                                          defaults=user_info)
            return (user, created)
        else:
            return (None, False)
login_manager.user_loader(lambda x: get_user(x)[0])


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = request.form['username'], request.form['password']
        if plugldap.login_user(username, password):
            user, created = get_user(username)
            flask_login.login_user(user)
            flash('Logged in successfully as %s %s (%s).' %
                  (user.first_name, user.last_name, user.id))
            user.last_login = datetime.datetime.utcnow()
            user.save(safe=False)
            if created or not user.country:
                resp = redirect(url_for('.profile',
                                        next=request.args.get('next', '')))
            else:
                resp = redirect(request.args.get("next") or
                                url_for('library.home'))
            resp.set_cookie("__ac",
                            base64.b64encode("%s:%s" % (username, password)))
            return resp
        else:
            flash('Bad username or password.')

    return render_template('login.html', form=form)


class Profile(views.MethodView):

    decorators = (flask_login.login_required,)

    def get(self):
        form = ProfileForm(obj=flask_login.current_user)
        return render_template('profile.html', form=form)

    def post(self, survey_id=None):
        form = ProfileForm()
        if form.validate():
            form.save(flask_login.current_user)
            flash('Profile updated successfully')
            return redirect(request.args.get("next") or url_for('library.home'))
        return render_template('profile.html', form=form)

auth.add_url_rule('/profile', view_func=Profile.as_view('profile'))


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
