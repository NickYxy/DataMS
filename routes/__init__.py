__author__ = 'nickyuan'
from models.user import User
from functools import wraps
from flask import (
    url_for,
    render_template,
    session,
    flash,
    redirect,
    Blueprint,
    request,
    g,
)


def current_user():
    uid = int(session.get('uid', -1))
    u = User.get(uid)
    return u


def add_g_user():
    uid = session.get('uid', -1)
    g.user = User.get(uid)


def add_g_data():
    data = {}
    data.update(request.args.to_dict())
    data.update(request.form.to_dict())

    data.pop('_', '')
    g.data = data


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_admin():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def t1_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_t_1():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def t2_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_t_2():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def t3_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_t_3():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def clients_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_clients():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function
