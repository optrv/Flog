import os
import sqlite3
import MySQLdb
from MySQLdb import escape_string as esc
from datetime import datetime
from flask import g
from flask_paginate import Pagination
from flog.configs.conf import (DATABASE, UPLOAD_FOLDER, ALLOWED_EXTENSIONS,
                               USERNAME, PASSWORD, POSTS_PER_PAGE, FORCE_SQLITE)
from flog.services.image_resizer.image_resizer import image_resizer
from flog.services.mp3_decoder.mp3_decoder import mp3_decoder
from werkzeug.utils import secure_filename

posts_per_page = int(POSTS_PER_PAGE)
force_sqlite = FORCE_SQLITE

def connect_mysql():
    try:
        db = MySQLdb.connect(host="localhost", port=3306, user="root",
                         passwd="root", db="posts", use_unicode=True, charset="utf8")
        cur = db.cursor()
        return db, cur
    except Exception:
        pass

def connect_db():
    """
    Connect with a database and use the sqlite3.Row-object
    """
    row = sqlite3.connect(DATABASE)
    row.row_factory = sqlite3.Row
    return row

def init_db():
    """
    Create the new database by schema.sql
    """
    db = get_db()
    with open(os.path.dirname(DATABASE) + '/schema.sql', mode = 'r') as s:
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
    if not os.path.exists(DATABASE):
        init_db()

def get_from_db():
    """
    Get the data from DB
    """
    sql_query = 'SELECT date_time, title, text, filename, filesave FROM posts ORDER BY id DESC'
    if not force_sqlite and connect_mysql():
        db, cur = connect_mysql()
        cur.execute(sql_query)
    else:
        check_db()
        db = get_db()
        cur = db.execute(sql_query)

    posts = cur.fetchall()
    db.close()
    return posts

def add_to_db(date_time, title, text, filename, filesave):
    """
    Add the data to DB
    """
    if date_time is None:
        date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if not force_sqlite and connect_mysql():
        db, cur = connect_mysql()
        cur.execute('INSERT INTO posts (date_time, title, text, filename, filesave) '
                    'VALUES (%s, %s, %s, %s, %s)', (date_time, title, text, filename, filesave))
    else:
        db = get_db()
        db.execute('INSERT INTO posts (date_time, title, text, filename, filesave) VALUES (?, ?, ?, ?, ?)',
                    [date_time, title, text, filename, filesave])
    db.commit()
    db.close()

def save_file(files):
    """
    Save the file
    """
    if files.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        date_time = datetime.now()
        filename = secure_filename(files.filename)
        hashname = date_time.strftime("%Y%m%d%H%M%S") + '.' + filename.rsplit('.', 1)[1]
        if filename.rsplit('.', 1)[1] != 'mp3':
            filesave = 'image_' + hashname
            subfolder = 'image/'
            image_resizer(files, filesave, subfolder)
        else:
            filesave = 'track_' + hashname
            subfolder = 'music/'
            mp3_decoder(files, filesave, subfolder)
        return filename, filesave, date_time.strftime("%Y/%m/%d %H:%M:%S")
    else:
        return None, None, None

def check_login(user_name, pass_word):
    """
    Check login/password
    """
    if (user_name != USERNAME or pass_word != PASSWORD):
        return False
    else:
        return True

def posts_page(page, posts):
    """
    Makes pagination of the posts
    """
    pagination = Pagination(page = page, per_page = posts_per_page, total = len(posts))
    i = (page - 1) * posts_per_page
    posts = posts[i:i + posts_per_page]
    return pagination, posts