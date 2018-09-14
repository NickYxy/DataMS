__author__ = 'nickyuan'

from models import MongoModel


class SubSystem(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            # 分系统名
            ('sys_name', str, ''),
            # 创建人uuid
            ('creator_uuid', str, ''),
            # 创建时间
            ('create_name', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @property
    def creator(self):
        from models.user import User
        u = User.get_uuid(self.creator_uuid)
        username = u.name if u else ''
        return username

    @classmethod
    def get_sub_system_name(cls, uuid):
        sub_system = cls.get_uuid(uuid)
        if sub_system is not None:
            return sub_system.sys_name
        else:
            return ''

    @classmethod
    def new(cls, form, **kwargs):
        m = super().new(form, **kwargs)
        m.save()
        return m

    def editable(self, u):
        # 管理员可以编辑所有的系统
        if u.is_admin():
            return True
        # 判读人员可以编辑自己权限内的系统
        else:
            return self.sys_name in u.privlist.keys() and 'edit' in u.privlist[self.sys_name]
