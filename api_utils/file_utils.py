import os
import typing

from flask import request


def allowed_file(filename: typing.Optional[str]) -> typing.Optional[bool]:
    if filename:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions
    return False


def save_form_file(path: str, name: str) -> None:
    image_file = request.files['image']
    if image_file and allowed_file(image_file.filename):
        image_file.save(os.path.join('static/img', path, name))
