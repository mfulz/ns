from app import app, db
from app.models import User, Domain
from app.login import login
from app.nsupdate import nsupdate
from app.validators import validate_ip, validate_domain
from flask import request, abort
from sqlalchemy import exc

@app.route("/ip")
def ip():
    return request.environ['REMOTE_ADDR']

@app.route("/update", methods=['POST'])
def update():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']
    _ip = request.form['ip']

    res = login(_username, _password)
    if res != 200:
        abort(res)

    if not validate_domain(_domain):
        abort(500)
    if not validate_ip(_ip):
        abort(500)

    user = User.query.filter_by(username=_username).first()
    if user == None:
        abort(500)

    domain = Domain.query.filter_by(domain=_domain,user_id=user.id).first()
    if domain == None:
        abort(500)

    if nsupdate(_ip, _domain) is not 0:
        abort(500)

    return "Success"

@app.route("/register_domain", methods=['POST'])
def register_domain():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']

    res = login(_username, _password)
    if res != 200:
        abort(res)

    if not validate_domain(_domain):
        abort(500)

    user = User.query.filter_by(username=_username).first()
    if user == None:
        user = User(username=_username)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.SQLAlchemyError, e:
            abort(500)

    domain = Domain(domain=_domain,user_id=user.id)

    try:
        db.session.add(domain)
        db.session.commit()
    except exc.SQLAlchemyError, e:
        abort(500)

    return "Success"

@app.route("/unregister_domain", methods=['POST'])
def unregister_domain():
    _username = request.form['username']
    _password = request.form['password']
    _domain = request.form['domain']

    res = login(_username, _password)
    if res != 200:
        abort(res)

    if not validate_domain(_domain):
        abort(500)

    user = User.query.filter_by(username=_username).first()
    if user == None:
        abort(500)

    domain = Domain.query.filter_by(domain=_domain,user_id=user.id).first()
    if domain == None:
        abort(500)

    try:
        db.session.delete(domain)
        db.session.commit()
    except exc.SQLAlchemyError, e:
        abort(500)

    return "Success"

