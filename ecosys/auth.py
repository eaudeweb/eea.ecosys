from flask import (Blueprint, request, render_template, redirect, url_for, flash)
from flask.ext.login import LoginManager
from flask.ext import wtf
from flask.ext import login as flask_login

from ecosys.forms import LoginForm
from ecosys.models import User
from ecosys import plugldap


auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = '.login'


def initialize_app(app):
    app.register_blueprint(auth)

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
            flash('Logged in successfully.')
            return redirect(request.args.get("next") or url_for('library.home'))
        else:
            flash('Bad username or password.')
    return render_template('login.html', form=form)


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('library.home'))
