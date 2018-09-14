from routes import *
from models.log import Log
from models.privilege import Privileges, get_all_privileges
from models.sub_system import SubSystem
from models.parameter import Parameter

main = Blueprint('user', __name__)


@main.route('/login')
def index():
    return render_template('user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    name = form.get('name', '')
    u = User.find_one(name=name)
    if u is not None and u.validate_login(form):
        session['uid'] = u.id
        Log.log(u, '登录账号', request, '[{}] 登录系统'.format(u.name))
        return redirect(url_for('index.index'))
    elif not u:
        flash('此用户未注册', 'warning')
        return redirect(url_for('user.index'))
    else:
        flash('用户名密码错误', 'warning')
        return redirect(url_for('user.index'))


@main.route('/register')
def register_page():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    status, msgs = User.valid(form)
    if status is True:
        u = User.new(form)
        session['uid'] = u.id
        flash('注册成功', 'success')
        Log.log(u, '注册账号', request, '[{}] 注册账号'.format(u.mobile))
        return redirect(url_for('user.index'))
    else:
        for msg in msgs:
            flash(msg, 'warning')
        return redirect(url_for('user.register'))


@main.route('/logout')
@login_required
def logout():
    session.pop('uid')
    flash('账号已安全退出', 'success')
    return redirect(url_for('index.index'))


# ------------------------- 权限模块 --------------------------


@main.route('/privilege_list')
@login_required
def privilege_list():
    u = current_user()
    ps = u.privlist
    return render_template('user/privilege_list.html', u=u, ps=ps)


@main.route('/privilege/apply')
@login_required
def privilege_apply_page():
    u = current_user()
    ms = SubSystem.all()
    ps = get_all_privileges()
    return render_template('user/privilege_apply.html', u=u, ms=ms, ps=ps)


@main.route('/privilege/apply', methods=['POST'])
@login_required
def privilege_apply():
    u = current_user()
    ms = SubSystem.all()
    ps = get_all_privileges()
    form = request.form
    return render_template('user/privilege_apply.html', u=u, ms=ms, ps=ps)


# ------------------------- 规程模块 --------------------------


@main.route('/parameters_list')
@login_required
def parameters_list_page():
    u = current_user()
    ms = SubSystem.all()
    ps = Parameter.all()
    return render_template('user/parameter_list.html', u=u, ms=ms, ps=ps)


@main.route('/parameters/add')
@login_required
def parameters_add_page():
    u = current_user()
    ms = SubSystem.all()
    return render_template('user/parameters_add.html', u=u, ms=ms)


@main.route('/parameters/add', methods=['POST'])
@login_required
def parameters_add():
    u = current_user()
    form = request.form
    SubSystem.new(form, creator_uuid=u.uuid)
    return redirect(url_for('user.parameters_list_page'))
