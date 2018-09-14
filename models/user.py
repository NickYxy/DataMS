__author__ = 'nickyuan'
import hashlib
from models import MongoModel


class User(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            # 姓名
            ('name', str, ''),
            # 登录密码
            ('password', str, ''),
            # 用户角色, 'admin'/'manager'/'user'/'t_1--t_3'
            ('role', str, 'user'),

            # 权限列表
            ('privlist', list, []),
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
            return user.name
        else:
            return ''

    @classmethod
    def new(cls, form):
        m = super().new(form)
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
        return self.role == 'admin'

    # 总师 -- 批准权限
    def is_t_1(self):
        return self.role == 't_1' or self.is_admin()

    # 指挥 -- 一级审核权限
    def is_t_2(self):
        return self.role == 't_2' or self.is_t_1()

    # 总体 -- 二级审核权限
    def is_t_3(self):
        return self.role == 't_3' or self.is_t_2()

    # 判读人员 -- 普通校对权限
    def is_user(self):
        return self.role == 'user'

    @classmethod
    def get_priv_list(self):
        return self.privlist

    @classmethod
    def get_proc_list(self):
        return self.proclist

    @classmethod
    def insert_admin(cls):
        u = User.find_one(name='admin')
        if not u:
            form = {
                'name': 'admin',
                'role': 'admin',
                'password': '123456'
            }
            cls.new(form)
