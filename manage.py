# -*- coding: utf-8 -*-
from app import create_app, db, loginmanager
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand, Migrate

# 导入数据库，必须在这里导入了之后create_all()才能创建表
from app.models import user, shop, personal, order, admin, role, address
from app.models.admin import Admin

app = create_app("default")
manage = Manager(app)
migrate = Migrate(app, db)


@loginmanager.user_loader
def load_user(id):
    return Admin.query.get(int(id))


def make_shell_contest():
    return dict(app=app, db=db, user_personal=user.user_personal, user_shop=user.user_shop, shop=shop.shop_info)


manage.add_command("runserver", Server(host="0.0.0.0", port=5001, use_reloader=False, use_debugger=True))
manage.add_command("shell", Shell(make_context=make_shell_contest))

# 用于数据库迁移的
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manage.run()
