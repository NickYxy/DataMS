from utils import path_for, make_dirs


class Config(object):
    # 未审批的资料文件夹
    FILE_DIR = path_for('static', 'files')

    # 已审批的资料文件夹
    APPROVED_FILE_DIR = path_for('static', 'approved_files')

    # 管理员的初始密码
    ADMIN_PASSWORD = '123456'

    # app secret key
    SECRET_KEY = 'you-never-know???'

    # 数据库相关设置
    DB_NAME = 'mongo_dataMS'
    DB_URL = 'mongodb://localhost:27017'


class DevelopmentConfig(object):
    ENV = 'development'
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True


def init_edu_project_dirs():
    dirs = [
        Config.FILE_DIR,
        Config.APPROVED_FILE_DIR,
    ]

    for name in dirs:
        make_dirs(name)
