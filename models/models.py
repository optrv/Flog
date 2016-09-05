from flog import app
from flask import g
import sqlite3
import os


def connect_db():
    """
    Connect with a database and use the sqlite3.Row-object
    """
    row = sqlite3.connect(app.config['DATABASE'])
    row.row_factory = sqlite3.Row
    return row

def init_db():
    """
    Create the new database by schema.sql
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('models/schema.sql', mode = 'r') as s:
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
    if not os.path.exists(app.config['DATABASE']):
        init_db()

def get_from_db():
    """
    Get the data from DB
    """
    check_db()
    db = get_db()
    cur = db.execute('SELECT title, text, file FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    return posts

def add_to_db(title, text, file):
    """
    Add the data to DB
    """
    db = get_db()
    db.execute('INSERT INTO posts (title, text, file) VALUES (?, ?, ?)',[title, text, file])
    db.commit()