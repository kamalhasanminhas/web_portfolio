from sqlalchemy import Enum

from models.db import db


class Project(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    technologies_used = db.Column(db.Text)
    project_url = db.Column(db.String(255))
    image = db.Column(db.String(255))

    # relations
    achievements = db.relationship('Achievement', lazy=True, cascade='all,delete')
    tools = db.relationship('Tool', lazy=True, cascade='all,delete')

    def __str__(self) -> str:
        return f'<Project {self.id}: {self.title}>'


class Achievement(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text, nullable=False)

    project = db.relationship('Project', lazy=True, overlaps="achievements")


class Tool(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    usage_context = db.Column(db.Text)

    project = db.relationship('Project', lazy=True, overlaps="tools")
