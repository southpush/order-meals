# -*- coding: utf-8 -*-
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand, Migrate

# 导入数据库，必须在这里导入了之后create_all()才能创建表
from app.models import user

app = create_app("default")
manage = Manager(app)
migrate = Migrate(app, db)


def make_shell_contest():
    return dict(app=app, db=db, user_personal=user.user_personal, user_shop=user.user_shop)


manage.add_command("runserver", Server(host="127.0.0.1", port=5000, use_reloader=True, use_debugger=True))
manage.add_command("shell", Shell(make_context=make_shell_contest))

# 用于数据库迁移的
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manage.run()
