from app import app, db
from app.models import User, Domain
from app.api_login import login
from app.nsupdate import nsupdate
from app.validators import validate_ip, validate_domain
from flask import request, abort, Blueprint
from sqlalchemy import exc


v1 = Blueprint('v1', __name__)


@v1.route("/ip")
def ip():
    return request.environ['REMOTE_ADDR']


@v1.route("/update", methods=['POST'])
def update():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']
    _ip = request.form['ip']

    res = login(_username, _password)
    if res != 200:
        return "Login failed"

    if not validate_domain(_domain):
        return "Invalid domain '{0}'".format(_domain)
    if not validate_ip(_ip):
        return "Invalid IP '{0}'".format(_ip)

    user = User.query.filter_by(username=_username).first()
    if user is None:
        return "Domain not registered '{0}'".format(_domain)

    domain = Domain.query.filter_by(domain=_domain, user_id=user.id).first()
    if domain is None:
        return "Domain not registered '{0}'".format(_domain)

    if nsupdate(_ip, _domain) is not 0:
        return "Something went wrong during update of '{0}' with IP '{1}'".format(
            _domain, _ip)

    return "Success"


@v1.route("/register_domain", methods=['POST'])
def register_domain():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']

    res = login(_username, _password)
    if res != 200:
        return "Login failed"

    if not validate_domain(_domain):
        return "Invalid domain '{0}'".format(_domain)

    user = User.query.filter_by(username=_username).first()
    if user is None:
        user = User(username=_username)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            return "Something went wrong during registration of domain '{0}'".format(
                _domain)

    domain = Domain(domain=_domain, user_id=user.id)
    try:
        db.session.add(domain)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return "Something went wrong during registration of domain '{0}'".format(
            _domain)

    return "Success"


@v1.route("/unregister_domain", methods=['POST'])
def unregister_domain():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']

    res = login(_username, _password)
    if res != 200:
        return "Login failed"

    if not validate_domain(_domain):
        abort(500)

    user = User.query.filter_by(username=_username).first()
    if user is None:
        return "User '{0}' doesn't have any domains".format(_username)

    domain = Domain.query.filter_by(domain=_domain, user_id=user.id).first()
    if domain is None:
        return "Domain '{0}' doesn't exist".format(_domain)

    try:
        db.session.delete(domain)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return "Something went wrong during unregistration of domain '{0}'".format(
            _domain)

    return "Success"
