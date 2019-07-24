import config.settings

from flask import Flask
from flask_script import Manager
from apps.todo.models import db
from apps.todo.views.todo import todo
from apps.todo.views.todo import login_manager
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
login_manager.login_view = 'todo.login'
login_manager.init_app(app)

# 注册路由
# register_view(app)

app.register_blueprint(todo, url_prefix='/todo')




if __name__ == '__main__':
    manager.run()
