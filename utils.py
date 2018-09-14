import os
import time
import maya
from uuid import uuid4


def epoch_of_now():
    return maya.now().epoch


def epoch_of_date(date):
    return maya.when(date, timezone='Asia/Shanghai').epoch


def epoch_of_tomorrow_date(date):
    return maya.when(date, timezone='Asia/Shanghai').add(days=1).epoch


def short_uuid():
    seed = str(uuid4())
    short_seed = seed.split('-')[-1]
    return short_seed


def project_path():
    utils_file = os.path.realpath(__file__)
    utils_dir = os.path.dirname(utils_file)
    root = os.path.join(utils_dir, os.pardir)
    root = os.path.abspath(root)
    return root


def path_for(*paths):
    """
    root = '/a'
    os.path.join(root, 'b', 'c.txt') -> /a/b/c.txt
    os.path.join(root, '/b', 'c.txt') -> /b/c.txt
    """
    root = project_path()
    path = os.path.join(root, *paths)
    path = os.path.abspath(path)
    return path


def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t) + 3600 * 8))


def user_role(role):
    d = {
        'admin': '系统管理员',
        't_1': '总师',
        't_2': '测试总体',
        't_3': '测试指挥',
        'user': '判读人员',
    }
    return d.get(role, '判读人员')


def priv_name(priv):
    d = {
        'edit': '编辑',
        'approve': '批准',
        'revision': '校对',
        'audit': '审核',
    }
    return d.get(priv, '')


def make_dirs(name):
    os.makedirs(name, exist_ok=True)


filters = {
    'time_str': time_str,
    'user_role': user_role,
    'priv_name': priv_name,
}
