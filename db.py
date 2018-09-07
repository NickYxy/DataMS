import sqlite3
from flask import _app_ctx_stack
from app import app

DATABASE = '/path/to/database.db'


# if you use Flask 0.9 or older you need to use flask._app_ctx_stack.top instead of g
# as the flask.g object was bound to the request and not application context.
def get_db():
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is None:
        db = _app_ctx_stack.topg._database = sqlite3.connect(DATABASE)
    return db


# Please keep in mind that the teardown request and appcontext functions are always executed,
# even if a before-request handler failed or was never executed.
# Because of this we have to make sure here that the database is there before we close it.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(_app_ctx_stack.top, '_database', None)
    if db is not None:
        db.close()
