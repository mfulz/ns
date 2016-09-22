from app import app, db
from app.models import User, Domain
from flask import request, abort, render_template
from flask_login import logout_user, login_required
from .forms.login import LoginForm
from .login.user import load_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title='Sign In',
                           form=form)
