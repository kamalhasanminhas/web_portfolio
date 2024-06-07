from wtforms import PasswordField, StringField, validators
from wtforms.form import Form


class LoginForm(Form):
    email = StringField(
        'Email or Username',
        [validators.InputRequired(message="Email is required")],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Password',
        [validators.InputRequired(message="Password is required")],
        render_kw={'class': 'form-control'}
    )
