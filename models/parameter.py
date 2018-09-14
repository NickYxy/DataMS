__author__ = 'nickyuan'
from models import MongoModel
from models.sub_system import SubSystem


class Parameter(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            # 参数名
            ('name', str, ''),
            # 参数值
            ('value', str, ''),
            # 所属分系统
            ('sub_system_uuid', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form, **kwargs):
        m = super().new(form, **kwargs)
        m.save()
        return m

    def update(self, form):
        super().update(form)
        self.save()
        return self

    @property
    def sub_system(self):
        s = SubSystem.find_one(uuid=self.sub_system_uuid)
        if s is not None:
            return s.sys_name
        else:
            return "无"

    def editable(self, u):
        # 管理员可以编辑所有的参数
        if u.is_admin():
            return True
        # 判读人员可以编辑自己权限内的参数
        else:
            return self.sub_system in u.privlist.keys() and 'edit' in u.privlist[self.sub_system]