from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from app import db
from app.model.pgsql.User import User

auth_ui = Blueprint('auth_ui', __name__)

# Embedded UI login endpoint
@auth_ui.route('/loginRequest', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    # check if user exists
    user = User.query.filter_by(email=email).first()

    # compare user password with the hashed password
    if not user or not user.verify_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('pages.login_page'))

    # flask-login make login
    login_user(user)

    # on user exists redirect to main
    return redirect(url_for('pages.main_page'))

# Embedded UI registration endpoint
@auth_ui.route('/registerRequest', methods=['POST'])
def register():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()

    # if exists redirect to
    if user:
        flash('Your e-mail is already registered, please login')
        return redirect(url_for('pages.login_page'))

    # init new user
    create_user = User(email=email, name=name, password=password)

    # add the new user to the database
    db.session.add(create_user)
    db.session.commit()

    return redirect(url_for('pages.login_page'))


@login_required
@auth_ui.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.login_page'))
