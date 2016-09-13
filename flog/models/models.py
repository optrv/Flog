import os
import sqlite3
from datetime import datetime
from flask import g
from flog.configs.conf import database, upload_folder, allowed_extensions, username, password
from flog.services.image_resizer.image_resizer import image_resizer
from flog.services.mp3_decoder.mp3_decoder import mp3_decoder

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
    cur = db.execute('SELECT date_time, title, text, filename, filesave FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    db.close()
    return posts

def add_to_db(date_time, title, text, filename, filesave):
    """
    Add the data to DB
    """
    if date_time is None:
        date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    db = get_db()
    db.execute('INSERT INTO posts (date_time, title, text, filename, filesave) '
               'VALUES (?, ?, ?, ?, ?)',[date_time, title, text, filename, filesave])
    db.commit()
    db.close()

def save_file(files):
    """
    Save the file
    """
    if files.filename.rsplit('.', 1)[1] in allowed_extensions:
        filename = files.filename
        date_time = datetime.now()
        hashname = date_time.strftime("%Y%m%d%H%M%S") + '.' + filename.rsplit('.', 1)[1]
        if filename.rsplit('.', 1)[1] != 'mp3':
            filesave = 'image_' + hashname
            subfolder = 'image/'
            image_resizer(files, filesave, subfolder)
        else:
            filesave = 'track_' + hashname
            subfolder = 'music/'
            mp3_decoder(files, filesave, subfolder)
        return filesave, date_time.strftime("%Y/%m/%d %H:%M:%S")
    else:
        return None, None

def check_login(user_name, pass_word):
    """
    Check login/password
    """
    if (user_name != username or pass_word != password):
        return False
    else:
        return True
