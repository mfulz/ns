from app import app
import ldap

def login(username, password):
    return 200
    dn = app.config['LDAP_CN'] + '=' + username + ',' + app.config['LDAP_BASEDN']
    ldap_filter = '(&(' + app.config['LDAP_CN'] + '=' + username + ')' + app.config['LDAP_FILTER'] + ')'
    try:
        l = ldap.initialize(app.config['LDAP_SERVER'])
        l.bind_s(dn, password, ldap.AUTH_SIMPLE)
        user = l.search_s(app.config['LDAP_BASEDN'], ldap.SCOPE_SUBTREE, ldap_filter, [app.config['LDAP_CN']])
        if len(user) != 1:
            abort(401)
        return 200
    except ldap.INVALID_CREDENTIALS:
        return 401
    except ldap.LDAPError, e:
        return 500

