import os.path
import typing

from flask import Blueprint, redirect, render_template, request
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug import Response

from api_utils.file_utils import allowed_file, save_form_file
from forms.user import LoginForm
from models.db import db
from models.education import Education
from models.experience import Experience
from models.project import Project
from models.skill import Skill
from models.user import User

user_bp = Blueprint('user_bp', __name__)


class LoginView(MethodView):
    template = 'login.html'

    def get(self) -> str:
        return render_template(
            self.template,
            is_authenticated=False,
            show_home_icon=True,
            show_login_icon=False,
            show_menu=False,
            form=LoginForm()
        )

    def post(self) -> typing.Union[str, Response]:
        form = LoginForm(request.form)
        if form.validate():
            user = User.get_user_by_email_or_username(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect('/')
        return render_template('login.html', error='Invalid Login Credentials', form=form)


@user_bp.route('/logout', methods=['GET'])
@login_required
def logout() -> Response:
    logout_user()
    return redirect('/')


user_bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
