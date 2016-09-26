import os
import unicodecsv as csv
import sqlite3
import MySQLdb
from datetime import datetime
from flask import g
from flask_paginate import Pagination
from flog.configs.conf import (DATABASE, DB_DUMP, UPLOAD_FOLDER, ALLOWED_EXTENSIONS,
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
    Connect to SQLite-db and use the sqlite3.Row-object
    """
    row = sqlite3.connect(DATABASE)
    row.row_factory = sqlite3.Row
    return row

def init_db():
    """
    Create the new SQLite-db by schema.sql
    """
    db = get_db()
    with open(os.path.dirname(DATABASE) + '/schema_sqlite.sql', mode = 'r') as s:
        db.cursor().executescript(s.read())
    db.commit()

def get_db():
    """
    Create the connection with the SQLite-db
    """
    try:
        g.sqlite_db
    except AttributeError:
        g.sqlite_db = connect_db()
    finally:
        return g.sqlite_db

def check_db(db):
    """
    Check if SQLite-db-file is exist
    """
    if not os.path.exists(DATABASE):
        init_db()
        read_dump(db)

def get_from_db():
    """
    Get the data from DB. MySQL is default db.
    SQlite is emergency db or it can be the main db with 'force_sqlite = True'
    """
    sql_query = 'SELECT date_time, title, text, filename, filesave FROM posts ORDER BY id DESC'
    if not force_sqlite and connect_mysql():
        db, cur = connect_mysql()
        cur.execute(sql_query)
    else:
        check_db()
        db = get_db()
        cur = db.execute(sql_query)
        #read_dump(db)
    posts = cur.fetchall()
    db.close()
    return posts

def read_dump(db):
    try:
        with open(DB_DUMP, 'rb') as dumpfile:
            dump = csv.DictReader(dumpfile)
            dump_rec = [(i['date_time'], i['title'], i['text'], i['filename'], i['filesave']) for i in dump]
            db.executemany('INSERT INTO posts (date_time, title, text, filename, filesave) VALUES (?, ?, ?, ?, ?)',
                           dump_rec)
            db.commit()
    except IOError:
        rows = ['date_time', 'title', 'text', 'filename', 'filesave']
        open_dump_file('w', rows)



def add_to_db(date_time, title, text, filename, filesave):
    """
    Add the data to DB. MySQL is default db.
    SQlite is emergency db or it can be the main db with 'force_sqlite = True'
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
    write_dump(date_time, title, text, filename, filesave)

def open_dump_file(mode, rows):
    """
    Open dump file
    """
    fp = open(DB_DUMP, mode)
    file_csv = csv.writer(fp)
    file_csv.writerow(rows)
    fp.close()

def write_dump(date_time, title, text, filename, filesave):
    """
    Append each added post to csv-file
    """
    if not os.path.exists(DB_DUMP):
        rows = ['date_time', 'title', 'text', 'filename', 'filesave']
        open_dump_file('w', rows)
    posts = [date_time, title, text, filename, filesave]
    # fp = open(DB_DUMP, 'a')
    # file_csv = csv.writer(fp)
    # file_csv.writerow(posts)
    open_dump_file('a', posts)

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