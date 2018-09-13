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
            # 参数列表
            ('paralist', int, 0),
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
