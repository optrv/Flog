from flog.configs.conf import database, upload_folder, allowed_extensions, username, password
from flask import g
from werkzeug.utils import secure_filename
import sqlite3
import os
from flog.services.image_resizer.image_resizer import image_resizer
from datetime import datetime

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
    Create the connection with the database
    """
    try:
        g.sqlite_db
    except AttributeError:
        g.sqlite_db = connect_db()
    finally:
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
    cur = db.execute('SELECT title, text, filename, date_time FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    return posts

def add_to_db(title, text, filename):
    """
    Add the data to DB
    """
    dates = str(datetime.date(datetime.now()))
    times = str(datetime.time(datetime.now()))
    date_time = dates + ' ' + times[:8]
    db = get_db()
    db.execute('INSERT INTO posts (title, text, filename, date_time) '
               'VALUES (?, ?, ?, ?)',[title, text, filename, date_time])
    db.commit()

def save_file(files):
    if files.filename.rsplit('.', 1)[1] in allowed_extensions:
        filename = secure_filename(files.filename)
        if filename.rsplit('.', 1)[1] != 'mp3':
            subfolder = 'image/'
            image_resizer(files, filename, subfolder)
        else:
            subfolder = 'music/'
            files.save(os.path.join(upload_folder, subfolder, files.filename))
        return True
    else:
        return False

def check_login(username, password):
    if (username != username or password != password):
        return False
    else:
        return True