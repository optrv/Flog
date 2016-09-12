import os
import sqlite3
from datetime import datetime
from flask import g
from flog.configs.conf import database, upload_folder, allowed_extensions, username, password
from flog.services.image_resizer.image_resizer import image_resizer
from flog.services.mp3_decoder.mp3_decoder import mp3_decoder
from werkzeug.utils import secure_filename

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
    date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
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
            mp3_decoder(files, filename, subfolder)
        return True
    else:
        return False

def check_login(user_name, pass_word):
    if (user_name != username or pass_word != password):
        return False
    else:
        return True
