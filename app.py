from config import (
    Config,
    DevelopmentConfig,
    init_edu_project_dirs,
    make_dirs, )
from flask import Flask
from routes import (
    add_g_user,
    add_g_data,
)


def init_app(env):
    app = Flask(__name__)
    app.config.from_object(Config)
    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    app = register_filters(app)
    app = register_routes(app)
    app.before_request(add_g_user)
    app.before_request(add_g_data)
    app = init_custom_commands(app)

    return app


def init_custom_commands(app):
    app.cli.command('init')(init_edu_project_dirs)
    return app


def register_routes(app):
    from routes.user import main as routes_user
    from routes.file import main as routes_file
    from routes.index import main as routes_index
    from routes.admin import main as routes_admin
    from routes.sub_system import main as routes_sub_system

    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_file, url_prefix='/file')
    app.register_blueprint(routes_index, url_prefix='/')
    app.register_blueprint(routes_admin, url_prefix='/admin')
    app.register_blueprint(routes_sub_system, url_prefix='/sub_system')

    return app


def register_filters(app):
    from utils import filters
    app.jinja_env.filters.update(filters)
    return app


def main():
    app = init_app('development')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    config = dict(
        host='0.0.0.0',
        port=8001,
    )

    app.run(**config)


if __name__ == '__main__':
    main()
