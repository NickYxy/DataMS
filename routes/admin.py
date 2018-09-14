from routes import *
from models.log import Log
from utils import user_role
from flask import (
    request,
    Blueprint,
    render_template,
    flash,
    url_for,
    redirect,
    jsonify,
)

main = Blueprint('admin', __name__)


@main.route('/user_list')
@admin_required
def user_list():
    ms = User.all()
    return render_template('admin/user_list.html', ms=ms)


@main.route('/user/add', methods=['POST'])
@admin_required
def user_add():
    form = request.form
    User.new(form, privlist={}, proclist=[])
    cu = current_user()
    d = dict(
        user_id=cu.id,
        user_name=cu.username,
        model='admin',
        action='user_new',
        content='管理员创建用户，用户：{}'.format(form.get('username')),
    )
    Log.new(d)
    return redirect(url_for('admin.user_list'))


@main.route('admin/user/<uuid>')
@admin_required
def user_json(uuid):
    m = User.find_one(uuid=uuid)
    return jsonify(m.json())


@main.route('/user/del/<uuid>')
@admin_required
def user_del(uuid):
    m = User.find_one(uuid=uuid)
    if m is not None:
        m.delete()
    return redirect(url_for('admin.user_list'))
