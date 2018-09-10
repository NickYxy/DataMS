from utils import path_for


class Config(object):
    # 未审批的资料文件夹
    FILE_DIR = path_for('static', 'files')

    # 已审批的资料文件夹
    APPROVED_FILE_DIR = path_for('static', 'approved_files')

    # 管理员的初始密码
    ADMIN_PASSWORD = '123456'
