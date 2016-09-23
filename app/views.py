from app import app, db
from app.models import User, Domain
from flask import request, abort, render_template, redirect
from flask_login import login_user, logout_user, login_required
from .forms.login import LoginForm
from .login.user import load_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # login needed
            print "OK"
            login_user(user)
            return redirect('/get_user?username={0}'.format(user.username))
        else:
            abort(401)
    return render_template('login.html',
                            title='Sign In',
                            form=form)

@app.route('/add_user', methods=['GET'])
@login_required
def add_user():
    user = User(username=request.args.get("username"))
    db.session.add(user)
    db.session.commit()
    return "OK"
    
@app.route('/get_user', methods=['GET'])
@login_required
def get_user():
    user = User.query.filter_by(username=request.args.get("username")).first()
    return str(user.id)
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')