import os.path
import typing
from uuid import uuid4

import PIL
from flask import redirect, request, url_for
from flask_admin import form
from flask_admin.contrib import sqla
from flask_admin.form import ImageUploadField
from flask_login import current_user
from flask_sqlalchemy.extension import Model  # type: ignore[attr-defined]
from markupsafe import Markup
from PIL.Image import Resampling
from sqlalchemy.orm.scoping import scoped_session
from werkzeug import Response
from werkzeug.datastructures import FileStorage
from wtforms.form import Form

from models.db import db
from models.project import Achievement, Project


class ImageUploadFieldPillowCompatible(ImageUploadField):
    def _resize(self, image: typing.Any, size: typing.Tuple[int, int, bool]) -> typing.Any:
        (width, height, _) = size
        small_img = image.resize((width, height), Resampling.LANCZOS)
        return small_img


class WebPortfolioModelView(sqla.ModelView):
    def __init__(
            self,
            model: typing.Type[Model],
            session: scoped_session[typing.Any],
            name: typing.Optional[str]=None,
            category: typing.Optional[str]=None,
            endpoint: typing.Optional[str]=None,
            url: typing.Optional[str]=None,
            **kwargs: typing.Any
    ) -> None:
        for k, v in kwargs.items():
            if k == 'form_columns' and 'id' in v:
                v.remove('id')
            setattr(self, k, v)
        super().__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self) -> bool:
        value: bool = current_user.is_authenticated
        return value

    def inaccessible_callback(self, name: str, **kwargs: typing.Any) -> Response:
        # redirect to login page if user doesn't have access
        return redirect(url_for('user_bp.login', next=request.url))


class ImageView(WebPortfolioModelView):
    @staticmethod
    def _list_thumbnail(view: sqla.ModelView, context: typing.Any, model: db.Model, name: str) -> str:  # type: ignore[name-defined]
        if not model.image:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=f'img/{form.thumbgen_filename(model.image)}'),)

    @staticmethod
    def image_name(obj: db.Model, file_data: FileStorage) -> str:  # type: ignore[name-defined]
        filename, extension = os.path.splitext(file_data.filename)  # type: ignore[type-var]
        return f"{filename}_{uuid4()}{extension}"

    column_formatters = {
        'image': _list_thumbnail
    }
    column_formatters_detail = {
        'image': _list_thumbnail
    }
    form_extra_fields = {
        'image': ImageUploadFieldPillowCompatible(
            'Image',
            base_path='static/img',
            url_relative_path='img/',
            thumbnail_size=(50, 50, True),
            namegen=image_name
        )
    }


class UserModelView(ImageView):
    can_create = False
    column_list = ('username', 'email', 'first_name',
                   'last_name', 'city', 'country',
                   'phone_number', 'job_title', 'image')


class ModelViewWithUserIdSet(WebPortfolioModelView):
    def on_model_change(self, form: Form, model: db.Model, is_created: bool) -> None:  # type: ignore[name-defined]
        """
            Perform some actions before a model is created or updated.

            Called from create_model and update_model in the same transaction
            (if it has any meaning for a store backend).

            By default does nothing.

            :param form:
                Form used to create/update model
            :param model:
                Model that will be created/updated
            :param is_created:
                Will be set to True if model was created and to False if edited
        """
        model.user_id = current_user.id


class ModelViewWithUserIdSetWithImage(ImageView, ModelViewWithUserIdSet):
    pass


class ToolModelView(WebPortfolioModelView):
    column_list = ['project', 'name']


class AchievementModelView(WebPortfolioModelView):
    column_list = ['project', 'description']
