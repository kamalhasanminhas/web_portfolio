import typing

from models.db import db


class Experience(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    achievements = db.Column(db.Text)
    image = db.Column(db.String(255))

    @property
    def achievement_list(self) -> typing.List[str]:
        achievement_split: typing.List[str] = self.achievements.split('\n')
        return achievement_split

    @property
    def responsibilities_list(self) -> typing.List[str]:
        resp_split: typing.List[str] = self.responsibilities.split('\n')
        return resp_split
