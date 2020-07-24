from __future__ import unicode_literals

from flask import Blueprint, render_template
from flask_login import login_required, current_user

pages_ui = Blueprint('pages', __name__)


@pages_ui.route('/')
@login_required
def main_page():
    return render_template('main.html', name=current_user.name)


@pages_ui.route('/byurl')
@login_required
def url_download_page():
    return render_template('downloadtools.html')


@pages_ui.route('/login')
def login_page():
    return render_template('login.html')


@pages_ui.route('/register')
def register_page():
    return render_template('register.html')


@pages_ui.route('/botadmin')
def botadmin_page():
    return render_template('botadmin.html')
