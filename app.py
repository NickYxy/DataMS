import sqlite3
from flask import (
    Flask,
    g,
)

db = ''
app = Flask(__name__)


def main():
    config = dict(
        host='0.0.0.0',
        port='8001',
    )

    app.jinja_env.auto_reload = True
    app.run(**config)


if __name__ == '__main__':
    main()
