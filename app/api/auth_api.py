from flask import Blueprint, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)

from app import db
from app.model.pgsql.User import User

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/loginApi', methods=['POST'])
def login():
    data = request.get_json(force=True)
    if not data.get('email') or not data.get('password'):
        response = {
            'message': 'email_and_password_field_are_required'
        }
        return jsonify(response), 400

    # check if user exists
    user = User.query.filter_by(email=data.get('email')).first()

    # compare user password with the hashed password
    if not user or not user.verify_password(data.get('password')):
        response = {
            'message': 'please_check_your_login_details'
        }
        return jsonify(response), 400

    # make login for UI access
    login_user(user)

    # create token
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    response = {
        'message': 'user_logged_in',
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonify(response), 200


@auth_api.route('/registerApi', methods=['POST'])
def register():
    data = request.get_json(force=True)
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    user = User.query.filter_by(
        email=email).first()

    # if exists response error
    if user:
        response = {
            'message': 'your_email_is_already_registered_please_login'
        }
        return jsonify(response), 400

    # init new user
    create_user = User(email=email, name=name, password=password)

    # add the new user to the database
    db.session.add(create_user)
    db.session.commit()

    response = {
        'message': 'user_registered_please_login_to_retrieve_token'
    }
    return jsonify(response), 200


@jwt_required
@auth_api.route('/logoutApi')
def logout_api():
    # logout from UI
    logout_user()

    # revoke token

    return redirect(url_for('pages.login_page'))
