import config.settings

from flask import Flask, redirect
from flask_script import Manager
from flask_login import LoginManager
from apps.todo.models import db, User
from apps.todo.views.todo import todo
app = Flask(__name__)
# 装载配置
app.debug = config.settings.DEBUG
app.config.update(config.settings.settings)
# 数据库
db.app = app
db.init_app(app)
# 打开之后可以重新建表
# db.drop_all()
db.create_all()

manager = Manager(app)

login_manager = LoginManager()
login_manager.init_app(app)

# 注册路由
# register_view(app)
app.register_blueprint(todo, url_prefix='/todo')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User.query.filter(User.id == id).first()
    if user:
        return user
    else:
        return None


if __name__ == '__main__':
    manager.run()
