# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Role
from flask_script import Manager, Shell


app = create_app("default")
manage = Manager(app)


def make_shell_contest():
    return dict(app=app, db=db, Role=Role)


manage.add_command("shell", Shell(make_context=make_shell_contest))


if __name__ == '__main__':
    manage.run()
