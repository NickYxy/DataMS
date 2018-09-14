__author__ = 'nickyuan'
from routes import *
from models.sub_system import SubSystem

main = Blueprint('sub_system', __name__)


@main.route('/list')
@login_required
def sub_system_list_page():
    u = current_user()
    systems = SubSystem.all()
    return render_template('user/sub_system_list.html', u=u, systems=systems)


@main.route('/sub_system/add', methods=['POST'])
@admin_required
def sub_system_add():
    u = current_user()
    form = request.form
    SubSystem.new(form, creator_uuid=u.uuid)
    return redirect(url_for('sub_system.sub_system_list_page'))


@main.route('/sub_system/del/<uuid>')
@admin_required
def sub_system_del(uuid):
    m = SubSystem.get_uuid(uuid)
    m.delete()
    flash('删除成功', 'success')
    return redirect(url_for('sub_system.sub_system_list_page'))
