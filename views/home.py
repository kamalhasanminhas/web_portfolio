from flask import Blueprint, render_template
from flask_login import current_user, login_required

from models.user import User

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def home() -> str:
    user = User.query.first()
    return render_template(
        'index.html',
        user=user,
        is_authenticated=current_user.is_authenticated,
        show_login_icon=True,
        show_menu=True
    )
