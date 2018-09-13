from routes import *
from models.log import Log

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
