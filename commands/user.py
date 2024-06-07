from getpass import getpass

import click
from flask.cli import AppGroup, with_appcontext

from exceptions.user import CannotCreateUser
from models.user import User

user_cli = AppGroup('user')


@user_cli.command('create')
@with_appcontext
def create_admin() -> None:
    user = User(
        username=click.prompt('Username', type=str),
        password=getpass('Password:'),
        email = click.prompt('Email', type=str),
        first_name = click.prompt('First Name', type=str),
        last_name = click.prompt('Last Name', type=str),
    )
    try:
        User.create(user)
    except CannotCreateUser:
        click.echo(click.style('Unable to create more users.', blink=True, bold=True, fg='red'), err=True)
    except Exception as e:
        click.echo(click.style('Unable to create user: %s' % e, blink=True, bold=True, fg='red'), err=True)
