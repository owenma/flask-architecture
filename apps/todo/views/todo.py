from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import abort
from apps.todo.views.forms import LoginForm, TodoForm
from flask_login import login_user, login_required, logout_user, LoginManager
from apps.todo.models import Todo, User, db


login_manager = LoginManager()

todo = Blueprint('todo', __name__)


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User.query.filter(User.id == id).first()
    if user:
        return user
    else:
        return None


@todo.route('/show_entries')
def show_entries():
    entries = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('show_entries.html', entries=entries)


@todo.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    form = TodoForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(Todo(title=request.form['title'], text=request.form['text']))
        db.session.commit()
        flash('成功推送新的任务！')
        return redirect(url_for('todo.show_entries'))
    else:
        flash('请填写标题和内容！')
        return redirect(url_for('todo.show_entries'))


@todo.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user:
            form = LoginForm(request.form)
            if form:
                # 将用户信息注册到flask-login中,*******重要
                login_user(user)

                if user.check_password(password):
                    session['logged_in'] = True
                    flash('你已经登录了')
                    return redirect(url_for('todo.show_entries'))
                else:
                    error = '密码不正确'
            else:
                error = '请填写内容'
        else:
            u = User()
            u.username = username
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            error = "用户名已经建立"

    return render_template('login.html', error=error)


@todo.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash('你已经登出了')
    return redirect(url_for('todo.show_entries'))


@todo.route('/delete', methods=['GET'])
def delete():
    if not session.get('logged_in'):
        abort(401)
    entry = Todo.query.get(request.args.get("id"))
    db.session.delete(entry)
    db.session.commit()
    flash('成功移除任务')
    return redirect(url_for('todo.show_entries'))


@todo.errorhandler(400)
def handler(exception):

    return '捕获到异常信息:%s' % exception


@todo.route('/make_abort/')
def get_abort():
    abort(400)
    return '终止'


