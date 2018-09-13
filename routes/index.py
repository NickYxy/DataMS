__author__ = 'nickyuan'
from . import *
from models.log import Log

main = Blueprint('index', __name__)


@main.route('/')
@login_required
def index():
    u = current_user()
    ms = Log.last(user_uuid=u.uuid, action='登录账号')
    return render_template('index.html', u=u, ms=ms)
