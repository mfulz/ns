import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

LDAP_SERVER = 'ldap://127.0.0.1'
LDAP_BASEDN = 'dc=domain,dc=org'
LDAP_CN = 'cn'
LDAP_FILTER = '(memberof=cn=ddnsgroup,ou=groups,dc=domain,dc=de)'

NSUPDATE_KEY = os.path.join(basedir, 'ns.key')
NSUPDATE_DOMAIN = 'domain.de'
NSUPDATE_SERVER = 'ns.domain.de'
NSUPDATE_TTL = 60
