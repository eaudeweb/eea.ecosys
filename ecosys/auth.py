from random import choice

import ldap

from flask.ext.login import LoginManager
from flask.ext import wtf

from ecosys.models import User


login_manager = LoginManager()
LDAP_SERVERS = [("ldap.eionet.europa.eu", 389),
                ("ldap2.eionet.europa.eu", 389),
                ("ldap3.eionet.europa.eu", 389),]
LDAP_ENCODING = 'utf-8'
LDAP_USER_DN = "uid=%s,ou=Users,o=EIONET,l=Europe"
LDAP_USER_SCHEMA = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
    'phone_number': 'telephoneNumber',
    'organisation': 'o',
    'uid': 'uid',
}

def connect_to_ldap():
    host, port = choice(LDAP_SERVERS)
    return ldap.open(host, port=port)

def ldap_user_info(username):
    """ Returns a dictionary of user information for user `username`.  """
    query_dn = LDAP_USER_DN % username
    ld = connect_to_ldap()
    try:
        result = ld.search_s(query_dn, ldap.SCOPE_BASE,
                    filterstr='(objectClass=organizationalPerson)',
                    attrlist=(LDAP_USER_SCHEMA.values()))
    except ldap.NO_SUCH_OBJECT:
        return None

    assert len(result) == 1
    dn, attr = result[0]
    assert dn == query_dn
    out = {}
    for name, ldap_name in LDAP_USER_SCHEMA.iteritems():
        if ldap_name in attr:
            out[name] = attr[ldap_name][0].decode(LDAP_ENCODING)
        else:
            out[name] = u""
    return out

def get_user(userid):
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        user_info = ldap_user_info(userid)
        if user_info:
            (user, created) = User.objects.get_or_create(id=user_info['uid'],
                                                          defaults=user_info)
            return user

@login_manager.user_loader
def load_user(userid):
    return get_user(userid)

def login_user(username, password):
    ld = connect_to_ldap()
    try:
        user_dn = LDAP_USER_DN % username
        ld.simple_bind_s(user_dn, password)
    except ldap.INVALID_CREDENTIALS:
        return False
    return get_user(username)


class LoginForm(wtf.Form):

    username = wtf.TextField('User ID', validators=[wtf.validators.Required()])

    password = wtf.PasswordField('Password',
                                 validators=[wtf.validators.Required()])
