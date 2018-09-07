import sqlite3
from flask import (
    Flask,
    g,
)

db = ''
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
