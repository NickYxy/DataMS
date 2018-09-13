__author__ = 'nickyuan'
from models import MongoModel


class Log(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('user_uuid', str, ''),
            ('user_name', str, ''),
            ('model', str, ''),
            ('action', str, ''),
            ('content', str, ''),
            ('user_agent', str, ''),
            ('ip', str, ''),
            ('platform', str, ''),
            ('browser', str, ''),
            ('version', str, ''),
            ('status', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def all(cls):
        ms = super().all()
        return ms

    @classmethod
    def search_or(cls, form):
        ms = super().search_or(form)
        return ms

    @classmethod
    def log(cls, user, action, request, content=None):
        ip = request.headers.get("X-real-ip")
        if ip is None:
            ip = request.remote_addr
        d = dict(
            user_uuid=user.uuid,
            user_name=user.name,
            action=action,
            ip=ip,
            content=content,
            platform=request.user_agent.platform,
            browser=request.user_agent.browser,
            version=request.user_agent.version,
            user_agent=request.user_agent.string,
        )
        Log.new(d)
