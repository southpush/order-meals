# -*- coding: utf-8 -*-
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell, Server

app = create_app("default")
manage = Manager(app)


def make_shell_contest():
    return dict(app=app, db=db, User=User)


manage.add_command("runserver", Server(host="127.0.0.1", port=5000, use_reloader=True, use_debugger=True))
manage.add_command("shell", Shell(make_context=make_shell_contest))


if __name__ == '__main__':
    manage.run()
