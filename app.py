import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from admin.webview import (AchievementModelView,
                           ModelViewWithUserIdSetWithImage, ToolModelView,
                           UserModelView)
from commands.user import user_cli
from models.db import db
from models.education import Education  # pylint: disable=unused-import
from models.experience import Experience  # pylint: disable=unused-import
from models.project import Achievement  # pylint: disable=unused-import
from models.project import Project, Tool
from models.skill import Skill  # pylint: disable=unused-import
from models.user import User
from models.hooks import del_image  # pylint: disable=unused-import
from views.home import home_bp
from views.user import user_bp

load_dotenv('app.env')

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.cli.add_command(user_cli)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)

admin = Admin(app, name='WebPortfolioAdmin', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelViewWithUserIdSetWithImage(Project, db.session))
admin.add_view(ModelViewWithUserIdSetWithImage(Education, db.session))
admin.add_view(ModelViewWithUserIdSetWithImage(Experience, db.session))
admin.add_view(ModelViewWithUserIdSetWithImage(Skill, db.session))
admin.add_view(AchievementModelView(Achievement, db.session))
admin.add_view(ToolModelView(Tool, db.session))


@login_manager.user_loader
def load_user(user_id: int) -> User:
    user: User = User.query.get(int(user_id))
    return user


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--create', action='store_true', help='Create Tables')
    args = parser.parse_args()
    if args.create:
        with app.app_context():
            db.create_all()
    app.run(debug=app.config.get('DEBUG', False))
