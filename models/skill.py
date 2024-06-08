import typing

from sqlalchemy import Enum

from models.db import db


class Skill(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    details = db.Column(db.Text)

    @property
    def details_list(self) -> typing.List[str]:
        detail_split: typing.List[str] = self.details.split('\n')
        return detail_split
