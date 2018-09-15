__author__ = 'nickyuan'
from werkzeug.datastructures import ImmutableMultiDict
from config import Config
from pymongo import (
    MongoClient,
    DESCENDING,
)
from utils import (
    short_uuid,
    epoch_of_date,
    epoch_of_now,
    epoch_of_tomorrow_date,
)


class MongoModel(object):
    db = MongoClient(Config.DB_URL)[Config.DB_NAME]

    @classmethod
    def _fields(cls):
        fields = [
            '_id',
            ('id', int, -1),
            ('uuid', str, ''),
            ('type', str, ''),
            ('deleted', bool, False),
            ('ct', int, 0),
            ('ut', int, 0),
        ]
        return fields

    @classmethod
    def _class_name(cls):
        return cls.__name__

    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None

    @classmethod
    def _next_id(cls):
        name = cls._class_name()
        id = cls.db[name].count() + 1
        return id

    def save(self):
        name = self._class_name()
        d = dict(
            filter={'uuid': getattr(self, 'uuid')},
            replacement=self.__dict__,
            upsert=True,
        )
        self.db[name].replace_one(**d)

    def set_uuid(self, field='uuid'):
        uuid = short_uuid()
        kwargs = {
            field: uuid,
        }

        while self.has(**kwargs):
            uuid = short_uuid()
            kwargs[field] = uuid

        setattr(self, field, uuid)
        self.save()

    @classmethod
    def new(cls, form=None, **kwargs):
        if form is None:
            form = {}

        m = cls()
        fields = cls._fields()
        fields.remove('_id')

        # 存储数据
        # form 来源于用户提交的数据
        # kwargs 来源于程序员手动添加的数据，比如 model 关联的 其它 uuid
        for field in fields:
            k, t, v = field
            if k in form:
                v = t(form[k])
                setattr(m, k, v)
            else:
                # 设置默认值
                setattr(m, k, v)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        m.id = cls._next_id()
        m.type = cls._class_name().lower()
        ts = epoch_of_now()
        m.ct = ts
        m.ut = ts
        m.set_uuid()
        m.save()
        return m

    @classmethod
    def get_uuid(cls, uuid):
        return cls.find_one(uuid=uuid)

    def update(self, form, hard=False):
        if isinstance(form, ImmutableMultiDict):
            form = form.to_dict()
        else:
            pass

        form['ut'] = epoch_of_now()
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)

        self.save()

    @classmethod
    def update_one(cls, uuid, form):
        m = cls.get_uuid(uuid)
        m.update(form)
        return m

    def delete(self):
        setattr(self, 'deleted', True)
        self.save()

    @classmethod
    def count(cls, **kwargs):
        kwargs['deleted'] = kwargs.pop('deleted', False)
        name = cls._class_name()
        number = cls.db[name].count(kwargs)
        return number

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        fields = cls._fields()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)

        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def last(cls, limit=5, **kwargs):
        kwargs['__limit'] = limit
        ms = cls.find(**kwargs)
        return ms

    @classmethod
    def get(cls, id):
        if isinstance(id, str):
            if id.isdigit():
                id = int(id)
                return cls.find_one(id=id)
            else:
                return None
        else:
            return cls.find_one(id=id)

    @classmethod
    def find(cls, **kwargs):
        kwargs['deleted'] = kwargs.pop('deleted', False)
        name = cls._class_name()
        docs = cls.db[name].find(kwargs)

        if '__sort' in kwargs:
            docs = docs.sort(kwargs['__sort'])
        else:
            # 默认是 按 id 字段 逆序排列
            docs = docs.sort('id', DESCENDING)

        limit = kwargs.pop('__limit', 10000)
        docs = docs.limit(limit)
        ms = [cls._new_with_bson(doc) for doc in docs]
        return ms

    @classmethod
    def find_one(cls, **kwargs):
        ms = cls.find(**kwargs)
        if len(ms) > 0:
            return ms[0]
        else:
            return None

    @classmethod
    def all(cls):
        return cls.find()

    @classmethod
    def find_or(cls, *args):
        conditions = {'$or': args}
        ms = cls.find(**conditions)
        return ms

    @classmethod
    def find_and(cls, *args):
        conditions = {'$and': args}
        ms = cls.find(**conditions)
        return ms

    @classmethod
    def search_or(cls, form):
        args = []
        for k, v in form.items():
            if isinstance(v, str) and v != '':
                # $i 忽略大小写
                arg = {k: {'$regex': v, '$options': '$i'}}
                args.append(arg)
            else:
                pass

        if len(args) > 0:
            return cls.find_or(*args)
        else:
            return cls.all()

    @classmethod
    def search_and(cls, form):
        args = []
        for k, v in form.items():
            if isinstance(v, str) and v != '':
                # _date_start/_date_end 的格式是 2018-09-01
                if k == '_date_start':
                    v = epoch_of_date(v)
                    args.append({'ct': {'$gte': v}})
                elif k == '_date_end':
                    v = epoch_of_tomorrow_date(v)
                    args.append({'ct': {'$lt': v}})
                else:
                    args.append({k: {'$regex': v, '$options': '$i'}})
            else:
                pass

        if len(args) > 0:
            return cls.find_and(*args)
        else:
            return cls.all()

    def json(self):
        d = self.__dict__
        d = {k: v for k, v in d.items() if k not in self.blacklist()}
        return d
