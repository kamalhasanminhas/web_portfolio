import logging
import typing

from flask_login import UserMixin
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from exceptions.user import CannotCreateUser
from models.db import db

logger = logging.getLogger(__name__)


class User(db.Model, UserMixin):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    profile_summary = db.Column(db.Text)
    image = db.Column(db.String(255))
    linked_in_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))

    # relations
    experiences = db.relationship('Experience', backref='user', lazy=True)
    educations = db.relationship('Education', backref='user', lazy=True)
    skills = db.relationship('Skill', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)

    @classmethod
    def can_crate_user(cls) -> bool:
        no_user: bool = cls.query.count() == 0
        return no_user

    @classmethod
    def get_user_by_email_or_username(cls, email_or_username: str) -> typing.Self:
        user: User = cls.query.filter(or_(User.email == email_or_username, User.username == email_or_username)).first()
        return user

    def set_password(self) -> None:
        self.password = generate_password_hash(self.password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def create(cls, user: typing.Self) -> typing.Self:
        if not cls.can_crate_user():
            raise CannotCreateUser("Only one user can be created.")
        user.set_password()
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            logger.error("Unable to create user: %s", e, exc_info=True)
            db.session.rollback()
            raise
