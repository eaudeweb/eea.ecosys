import flask

from random import choice

import ldap

#LDAP_SERVERS = [("ldap.eionet.europa.eu", 389),
#                ("ldap2.eionet.europa.eu", 389),
#                ("ldap3.eionet.europa.eu", 389),]
#LDAP_ENCODING = 'utf-8'
#LDAP_USER_DN = "uid=%s,ou=Users,o=EIONET,l=Europe"
#LDAP_USER_SCHEMA = {
#    'first_name': 'givenName',
#    'last_name': 'sn',
#    'email': 'mail',
#    'phone_number': 'telephoneNumber',
#    'organisation': 'o',
#    'uid': 'uid',
#}


def get_ldap_cfg():
    app = flask.current_app
    cfg = {}
    for key in ('LDAP_SERVERS', 'LDAP_ENCODING', 'LDAP_USER_DN',
                'LDAP_USER_SCHEMA'):
        cfg[key] = app.config[key]
    return cfg


def connect_to_ldap(ldap_servers):
    host, port = choice(ldap_servers)
    return ldap.open(host, port=port)


def user_info(username):
    """ Return a dictionary of user information for user `username` """
    cfg = get_ldap_cfg()
    query_dn = cfg['LDAP_USER_DN'] % username
    ld = connect_to_ldap(cfg['LDAP_SERVERS'])
    try:
        result = ld.search_s(query_dn, ldap.SCOPE_BASE,
                    filterstr='(objectClass=organizationalPerson)',
                    attrlist=(cfg['LDAP_USER_SCHEMA'].values()))
    except ldap.NO_SUCH_OBJECT:
        return None

    assert len(result) == 1
    dn, attr = result[0]
    assert dn == query_dn
    out = {}
    for name, ldap_name in cfg['LDAP_USER_SCHEMA'].iteritems():
        if ldap_name in attr:
            out[name] = attr[ldap_name][0].decode(cfg['LDAP_ENCODING'])
        else:
            out[name] = u""
    return out


def login_user(username, password):
    cfg = get_ldap_cfg()
    ld = connect_to_ldap(cfg['LDAP_SERVERS'])
    try:
        user_dn = cfg['LDAP_USER_DN'] % username
        ld.simple_bind_s(user_dn, password)
    except ldap.INVALID_CREDENTIALS:
        return False
    return True
