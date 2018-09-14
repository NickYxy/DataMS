__author__ = 'nickyuan'
import hashlib
from models import MongoModel


class User(MongoModel):
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

    @classmethod
    def get_username(cls, uuid):
        user = cls.get_uuid(uuid)
        if user is not None:
            return user.username
        else:
            return ''

    @classmethod
    def new(cls, form, **kwargs):
        m = super().new(form, **kwargs)
        m.password = m.salted_password(form.get('password', ''))
        m.save()
        return m

    def validate_login(self, form):
        password = form.get('password', '')
        password = self.salted_password(password)
        return password == self.password

    def salted_password(self, password):
        salt = self.salt
        hash1 = hashlib.sha1(password.encode('ascii')).hexdigest()
        hash2 = hashlib.sha1((hash1 + salt).encode('ascii')).hexdigest()
        return hash2

    @classmethod
    def valid(cls, form):
        name = form.get('name', '')
        password = form.get('password', '')
        valid_user = cls.find_one(name=name) is None
        valid_password = len(password) >= 3
        msgs = []
        if not valid_user:
            message = '用户名已存在'
            msgs.append(message)
        if not valid_password:
            message = '密码至少需要三位数'
            msgs.append(message)
        status = valid_user and valid_password
        return status, msgs

    def is_admin(self):
        return self.role == '管理员'

    # 总师 -- 批准权限
    def is_t_1(self):
        return self.role == '总师' or self.is_admin()

    # 指挥 -- 一级审核权限
    def is_t_2(self):
        return self.role == '测试指挥' or self.is_t_1()

    # 总体 -- 二级审核权限
    def is_t_3(self):
        return self.role == '测试总体' or self.is_t_2()

    # 判读人员 -- 普通校对权限
    def is_user(self):
        return self.role == '判读人员'

    @classmethod
    def insert_admin(cls):
        u = User.find_one(name='admin')
        if not u:
            form = {
                'name': 'admin',
                'username': 'admin',
                'role': '管理员',
                'password': '123456',
            }
            cls.new(form, privlist={'测试系统一': ['edit', 'revision', 'audit', 'approve'],
                                    '测试系统二': ['edit'],
                                    '测试系统三': ['edit'],
                                    '测试系统四': ['edit']
                                    },
                    proclist=[])
