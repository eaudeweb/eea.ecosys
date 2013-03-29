from flask.ext.login import LoginManager
from flask.ext import wtf

from ecosys.models import User
from ecosys import plugldap


login_manager = LoginManager()
login_manager.login_view = '.login'


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


@login_manager.user_loader
def load_user(userid):
    # for some reason the decorator makes this method unusable otherwise
    return get_user(userid)


class LoginForm(wtf.Form):

    username = wtf.TextField('User ID', validators=[wtf.validators.Required()])

    password = wtf.PasswordField('Password',
                                 validators=[wtf.validators.Required()])
