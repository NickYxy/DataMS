__author__ = 'nickyuan'
from models import MongoModel


class Process(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            # 账号
            ('name', str, ''),
            # 姓名
            ('username', str, ''),
            # 登录密码
            ('password', str, ''),
            # 用户角色, 'admin'/'manager'/'user'/'t_1--t_3'
            ('role', str, 'user'),

            # 权限列表
            ('privlist', dict, {}),
            # 进程列表
            ('proclist', list, []),
            # 用户密码的盐、
            ('salt', str, '123456'),

        ]
        fields.extend(super()._fields())
        return fields
