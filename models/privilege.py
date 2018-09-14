__author__ = 'nickyuan'

from enum import Enum


class Privileges(Enum):
    # 编辑
    edit = '编辑'
    # 校对
    revision = '校对'
    # 审核
    audit = '审核'
    # 批准
    approve = '批准'


def get_all_privileges():
    ps = []
    for privilege in Privileges:
        ps.append(privilege)
    return ps
