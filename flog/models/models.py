from flog import app
import os
import ConfigParser
import sqlite3
from flask import g

config = ConfigParser.ConfigParser()
config.read(os.path.join(app.root_path, '../flog.conf'))
database = os.path.join(app.root_path, config.get('PATH', 'DATABASE'))
secret_key = config.get('AUTH', 'SECRET_KEY')
username = config.get('AUTH', 'USERNAME')
password = config.get('AUTH', 'PASSWORD')
debug = config.get('ETC', 'DEBUG')

app.config.update(DATABASE = database,
                  SECRET_KEY = secret_key,
                  USERNAME = username,
                  PASSWORD = password,
                  DEBUG = debug)

def connect_db():
    """
    Connect with a database and use the sqlite3.Row-object
    """
    row = sqlite3.connect(database)
    row.row_factory = sqlite3.Row
    return row

def init_db():
    """
    Create the new database by schema.sql
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('models/schema.sql', mode='r') as s:
            db.cursor().executescript(s.read())
        db.commit()

def get_db():
    """
    Create the database and connection with the database
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def check_db():
    """
    Check if db-file is exist
    """
    if not os.path.exists(database):
        init_db()
