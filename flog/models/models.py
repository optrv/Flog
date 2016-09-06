from flog.configs.conf import database
from flask import g
import sqlite3
import os

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
    db = get_db()
    with open(os.path.dirname(database) + '/schema.sql', mode = 'r') as s:
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