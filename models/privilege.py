__author__ = 'nickyuan'

from enum import Enum


class Privileges(Enum):
    # 编辑
    edit = 1
    # 校对
    revision = 2
    # 审核
    audit = 3
    # 批准
    approve = 4
