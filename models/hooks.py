import os
import typing

from flask_admin import form
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper
from sqlalchemy.engine.base import Connection

from models.db import db
from models.education import Education
from models.experience import Experience
from models.project import Project
from models.user import User


@listens_for(Project, 'after_delete')
@listens_for(User, 'after_delete')
@listens_for(Experience, 'after_delete')
@listens_for(Education, 'after_delete')
def del_image(mapper: Mapper[typing.Any], connection: Connection, target: db.Model) -> None:  # type: ignore[name-defined]
    # Delete image
    try:
        os.remove(os.path.join('static/img', target.image))
    except OSError:
        pass
    # Delete thumbnail
    try:
        os.remove(os.path.join('static/img', form.thumbgen_filename(target.image)))
    except OSError:
        pass
